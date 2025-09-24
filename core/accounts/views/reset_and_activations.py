from django.shortcuts import render
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from http import HTTPStatus
from django.contrib.auth import get_user_model

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
        target_user = User.objects.filter()
        if not target_user.exists():
            return render(
                request,
                "accounts/reset-and-activation/password_reset.html",
                context={
                    "error":"User not found."
                },
                status=HTTPStatus.NOT_FOUND,
            )
        

class PasswordResetConfirm(View):
    pass

class Activate(View):
    pass