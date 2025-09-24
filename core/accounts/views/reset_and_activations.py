from django.shortcuts import render
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from http import HTTPStatus
from django.contrib.auth import get_user_model, authenticate
from accounts.tasks import send_confirm_code_mail
from accounts.models import ConfirmCode
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

# Reset and Activation
class PasswordReset(View):
    def get(self,request):
        return render(
            request,
            "accounts/reset-and-activation/password_reset.html",
        )
    
    def post(self,request):
        email = request.POST.get("email",'')
        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            return render(
                request,
                "accounts/reset-and-activation/password_reset.html",
                context={
                    "error":"Email is invalid."
                },
                status=HTTPStatus.BAD_REQUEST
            )
        # Check if user is exists
        target_user = User.objects.filter(email=email)
        if not target_user.exists():
            return render(
                request,
                "accounts/reset-and-activation/password_reset.html",
                context={
                    "error":"User not found."
                },
                status=HTTPStatus.NOT_FOUND,
            )
        else:
            target_user = target_user.first()
        # Send mail
        send_confirm_code_mail.delay(target_user.email)
        return render(
            request,
            "accounts/reset-and-activation/password_reset.html",
            context={
                "data":"Confirm code sent."
            },
            status=HTTPStatus.OK,
        )

class PasswordResetConfirm(View):
    def get(self,request,code):
        confirm_code = ConfirmCode.objects.filter(code=code)
        # Check if user is exist or not
        if not confirm_code.exists():
            return render(
                request,
                "accounts/reset-and-activation/password_reset_confirm.html",
                context={
                    "error": "Confirm code not found."
                },
                status=HTTPStatus.NOT_FOUND,
            )
        # Return template
        return render(
            request,
            "accounts/reset-and-activation/password_reset_confirm.html",
            status=HTTPStatus.OK,
        )
    
    def post(self,request,code):
        confirm_code = ConfirmCode.objects.filter(code=code)
        password = request.POST.get("password","")
        password_confirm = request.POST.get("password_confirm","")
        # validate password
        try:
            validate_password(password)
        except ValidationError:
            return render(
                request,
                "accounts/reset-and-activation/password_reset_confirm.html",
                context={
                    "error": "Password is invalid."
                },
                status=HTTPStatus.BAD_REQUEST,
            )
        # Check if user is not exist
        if not confirm_code.exists():
            return render(
                request,
                "accounts/reset-and-activation/password_reset_confirm.html",
                context={
                    "error": "Confirm code not found."
                },
                status=HTTPStatus.NOT_FOUND,
            )
        else:
            confirm_code = confirm_code.first()
        # Check password 
        if password != password_confirm:
            return render(
                request,
                "accounts/reset-and-activation/password_reset_confirm.html",
                context={
                    "error": "Password and password_confirm are not same."
                },
                status=HTTPStatus.BAD_REQUEST,
            )
        # Reset password
        email=confirm_code.user.email
        user = User.objects.filter(email=email).first()
        user.set_password(password)
        user.save()
        return render(
            request,
            "accounts/reset-and-activation/password_reset_confirm.html",
            context={
                "data":"Password successfully reset."
            },
            status=HTTPStatus.OK
        )


class Activate(View):
    def get(self,request,user_slug):
        user = User.objects.filter(user_slug=user_slug)
        # Check if user is exists
        if not user.exists():
            return render(
                request,
                "accounts/reset-and-activation/activation.html",
                context={
                    "error":"User not found."
                },
                status=HTTPStatus.NOT_FOUND
            )
        else: 
            user = user.first()
        # Send email
        send_confirm_code_mail.delay(user.email)
        return render(
            request,
            "accounts/reset-and-activation/activation.html",
        )
    
    def post(self,request,user_slug):
        code = request.POST.get("code","")
        password = request.POST.get("password","")
        user = User.objects.filter(user_slug=user_slug)
        # Check if user is exists
        if not user.exists():
            return render(
                request,
                "accounts/reset-and-activation/activation.html",
                context={
                    "error":"User not found."
                },
                status=HTTPStatus.NOT_FOUND
            )
        else:
            user = user.first()
            # Check confirm code is exist
            confirm_code = ConfirmCode.objects.filter(code=code,user=user)
            if not confirm_code.exists():
                return render(
                request,
                "accounts/reset-and-activation/activation.html",
                context={
                    "error":"Wrong user wants to be activated."
                },
                status=HTTPStatus.FORBIDDEN
            )
            confirm_code = confirm_code.first()
        # check password of user
        if not user.check_password(password):
            return render(
                request,
                "accounts/reset-and-activation/activation.html",
                context={
                    "error":"Password is incorrect."
                },
                status=HTTPStatus.FORBIDDEN
            )
        # Activate user and delete activation code
        user.is_active = True
        user.save()
        confirm_code.delete()
        return render(
            request,
            "accounts/reset-and-activation/activation.html",
            context={
                "data":"User activated."
            }
        )