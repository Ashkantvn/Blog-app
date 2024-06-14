from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.shortcuts import render

def users_login_view(request):
    form = AuthenticationForm()
    return render(request,"users/users_login.html",{"form":form})

def users_register_view(request):
    form = UserCreationForm()
    return render(request,"users/users_register.html",{"form" : form})


def users_logout_view(request):
    pass