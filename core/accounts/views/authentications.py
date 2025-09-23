from django.views import View
from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login, logout
from http import HTTPStatus
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q

User = get_user_model()

# Authentication
class Login(View):
    def get(self,request):
        return render(
            request,
            "accounts/authentications/login.html",
        )
    
    def post(self,request):
        email = request.POST.get("email","")
        password = request.POST.get("password","")


        user = authenticate(request,username=email,password=password)
        # Check if user is exists or not
        if user is None:
            return render(
                request,
                "accounts/authentications/login.html",
                context={
                    "error":"User not found."
                },
                status=HTTPStatus.NOT_FOUND,
            )
        
        login(request,user)
        return render(
            request,
            "accounts/authentications/login.html",
            context={
                "data": {
                    "username": user.username
                },
            },
            status=HTTPStatus.OK
        )

class Logout(View):
    # Check permission method
    def check_permission(self, request):
        # Check if user is logged in
        if not request.user.is_authenticated:
            return render(
                request,
                "accounts/authentications/logout.html",
                context={
                    "error":"You must be logged in to access this page."
                },
                status=HTTPStatus.UNAUTHORIZED
            )
        return None

    def get(self,request):
        check_permission = self.check_permission(request)
        if check_permission:
            return check_permission
        return render(
            request,
            "accounts/authentications/logout.html",
        )
    
    def post(self,request):
        check_permission = self.check_permission(request)
        if check_permission:
            return check_permission
        logout(request)
        return render(
            request,
            "accounts/authentications/logout.html",
            context={
                "data":"Successfully logged out."
            },
            status=HTTPStatus.OK
        )
        

    

class SignUp(View):
    def get(self,request):
        return render(
            request,
            "accounts/authentications/signup.html",
        )

    def post(self,request):
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        username = request.POST.get("username","")
        first_name = request.POST.get("first_name","")
        last_name = request.POST.get("last_name","")

        # Check if first name and last name is exist
        if not first_name:
            return render(
                request,
                "accounts/authentications/signup.html",
                context={
                    "error":"First name are required."
                },
                status=HTTPStatus.BAD_REQUEST
            )

        user = User.objects.filter(Q(email=email)|Q(username=username))
        # Check if user is exist
        if user.exists():
            return render(
                request,
                "accounts/authentications/signup.html",
                context={
                    "error":"User exists."
                },
                status=HTTPStatus.FORBIDDEN
            )
        
        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            return render(
                request,
                "accounts/authentications/signup.html",
                context={
                    "error":"Email validation error."
                },
                status=HTTPStatus.BAD_REQUEST
            )
        
        # Check password validation
        try:
            validate_password(password)
        except:
            return render(
                request,
                "accounts/authentications/signup.html",
                context={
                    "error":"Password validation error."
                },
                status=HTTPStatus.BAD_REQUEST
            )
        
        # User creation
        created_user = User.objects.create_user(
            email=email,
            username=username,
            first_name = first_name,
            last_name = last_name,
            password=password
        )
        login(request,created_user)
        return render(
            request,
            "accounts/authentications/signup.html",
            context={
                "data":username
            },
            status= HTTPStatus.CREATED
        )
        
