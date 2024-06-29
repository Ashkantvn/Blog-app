from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from posts import models as posts_model



def users_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if  form.is_valid():
            login(request, form.get_user())
            return redirect("users:info")
    else:
        form = AuthenticationForm
    return render(request,"users/users_login.html",{"form":form})

def users_register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request,form.save())
            return redirect("users:info")
    else:
        form = UserCreationForm()
    return render(request,"users/users_register.html",{"form" : form})


def users_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("users:login")




@login_required(login_url="/users/login")
def users_view(request):
    users_posts = posts_model.Post.objects.filter(author = request.user)
    context = {"user_posts":users_posts}
    return render(request,"users/users_info.html",context)