from django.views import View
from django.shortcuts import render
from core.mixins import CustomLoginRequiredMixin
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


User = get_user_model()


# Account management
class UpdateAccount(CustomLoginRequiredMixin, View):
    permission_denied_template = "accounts/account-management/update.html"

    def get(self, request):
        return render(
            request,
            "accounts/account-management/update.html",
            status=HTTPStatus.OK
        )

    def post(self, request):
        user = request.user
        # Fields
        email = request.POST.get("email", request.user.email)
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")
        first_name = request.POST.get("first_name", request.user.first_name)
        last_name = request.POST.get("last_name", request.user.last_name)
        profile_image = request.FILES.get(
            "profile_image",
            request.user.profile_image
        )
        username = request.POST.get("username", request.user.username)
        # Check if all fields exists
        if not all([email, first_name, last_name, profile_image, username]):
            return render(
                request,
                "accounts/account-management/update.html",
                context={"error": "All fields are required."},
                status=HTTPStatus.BAD_REQUEST,
            )
        # Check if password and confirm password match
        if password:
            if password == password_confirm:
                user.set_password(password)
            else:
                return render(
                    request,
                    "accounts/account-management/update.html",
                    context={
                        "error":
                            "Password and Confirm Password do not match.",
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )
        # Validate email and password
        try:
            validate_email(email)
            # Validate password only if it is being changed
            if password:
                validate_password(password)
        except ValidationError:
            return render(
                request,
                "accounts/account-management/update.html",
                context={"error": "Invalid password or email."},
                status=HTTPStatus.BAD_REQUEST,
            )
        # Update user data
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.profile_image = profile_image
        user.username = username
        user.save()
        return render(
            request,
            "accounts/account-management/update.html",
            context={
                "data": "User successfully updated",
            },
            status=HTTPStatus.OK,
        )


class Profile(View):
    def get(self, request, user_slug):
        # Check current user and target user are the same
        if request.user.is_authenticated:
            current_user = request.user
            if current_user.user_slug == user_slug:
                return render(
                    request,
                    "accounts/account-management/profile.html",
                    context={
                        "data": request.user,
                    },
                    status=HTTPStatus.OK,
                )
        # Query to find target user
        target_user = User.objects.filter(user_slug=user_slug)
        if target_user.exists():
            return render(
                request,
                "accounts/account-management/profile.html",
                context={
                    "data": target_user.first(),
                },
                status=HTTPStatus.OK,
            )
        # Return 404
        return render(
            request,
            "accounts/account-management/profile.html",
            context={
                "error": "User not found.",
            },
            status=HTTPStatus.NOT_FOUND,
        )


class DeleteAccount(View):

    def get(self, request):
        # Check user is authenticated
        if not request.user.is_authenticated:
            return render(
                request,
                "accounts/account-management/delete.html",
                context={
                    "error": "You must be logged in."
                },
                status=HTTPStatus.UNAUTHORIZED,
            )
        # Render page
        return render(
            request,
            "accounts/account-management/delete.html",
            status=HTTPStatus.OK
        )

    def post(self, request):
        # Check user is authenticated
        if not request.user.is_authenticated:
            return render(
                request,
                "accounts/account-management/delete.html",
                context={"error": "You must be logged in."},
                status=HTTPStatus.UNAUTHORIZED,
            )
        username = request.user.username
        # Delete user
        request.user.delete()
        return render(
            request,
            "accounts/account-management/delete.html",
            context={"data": f"{username} deleted."},
        )
