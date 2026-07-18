from django.utils import timezone
from datetime import timedelta
import secrets

from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, authenticate, login, logout
from http import HTTPStatus
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from accounts.models.confirm_code import ConfirmCode
from accounts.tasks import send_confirm_code_mail
from core.mixins import CustomLoginRequiredMixin

User = get_user_model()


# Authentication
class Login(View):
    def get(self, request):
        return render(
            request,
            "accounts/authentications/login.html",
        )

    def post(self, request):
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)

        # Check if user is authenticated or not
        if user is None:
            return render(
                request,
                "accounts/authentications/login.html",
                context={"error": "User not found."},
                status=HTTPStatus.NOT_FOUND,
            )
        else:        
            if user.is_active:
                # Login user
                login(request, user)   
                return render(
                    request,
                    "accounts/authentications/login.html",
                    context={"data": user.username},
                    status=HTTPStatus.OK,
                )
            else:
                # Send activation email if user is not activated and redirect to activation page
                confirm_code = ConfirmCode.objects.filter(user=user).first()
                if confirm_code and timezone.now() - confirm_code.updated_date < timedelta(minutes=3):
                    return redirect("accounts:activate", user_slug=user.user_slug)
                else:
                    code = secrets.token_urlsafe(8)
                    ConfirmCode.objects.update_or_create(
                        user=user,
                        defaults={"code": code},
                    )
                    
                    send_confirm_code_mail.using(queue_name="emails").enqueue(
                        user.email, 
                        code
                    )
                    return redirect("accounts:activate", user_slug=user.user_slug)


class Logout(CustomLoginRequiredMixin, View):
    permission_denied_template = "accounts/authentications/logout.html"

    def get(self, request):
        return render(
            request,
            "accounts/authentications/logout.html",
        )

    def post(self, request):
        logout(request)
        return render(
            request,
            "accounts/authentications/logout.html",
            context={"data": "Successfully logged out."},
            status=HTTPStatus.OK,
        )


class SignUp(View):
    def get(self, request):
        return render(
            request,
            "accounts/authentications/signup.html",
        )

    def post(self, request):
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")
        username = request.POST.get("username", "")
        profile_image = request.FILES.get("profile_image")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        # Check if required fields is exist
        if not all([first_name, email, password_confirm, password, username]):
            return render(
                request,
                "accounts/authentications/signup.html",
                context={"error": "Enter all required fields."},
                status=HTTPStatus.BAD_REQUEST,
            )
        user = User.objects.filter(Q(email=email) | Q(username=username))
        # Check if user is exist
        if user.exists():
            return render(
                request,
                "accounts/authentications/signup.html",
                context={"error": "User exists."},
                status=HTTPStatus.FORBIDDEN,
            )
        # Check if password and password_confirm are the same
        if password != password_confirm:
            return render(
                request,
                "accounts/authentications/signup.html",
                context={
                    "error":
                        "password and password_confirm must be same."
                },
            )
        # Validate email nad password
        try:
            validate_email(email)
            validate_password(password)
        except ValidationError:
            return render(
                request,
                "accounts/authentications/signup.html",
                context={"error": "Invalid password or email."},
                status=HTTPStatus.BAD_REQUEST,
            )
        # User creation
        data = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
        }
        if profile_image:
            data["profile_image"] = profile_image
        User.objects.create_user(**data)
        return redirect("accounts:login")
