from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,PasswordChangeForm
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
        form = AuthenticationForm()
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

@login_required(login_url="/users/login")
def users_logout_view(request):
    logout(request)
    return redirect("users:login")




@login_required(login_url="/users/login")
def users_view(request):
    users_posts = posts_model.Post.objects.filter(author = request.user)
    uesrs_comments = posts_model.Comment.objects.filter(author = request.user)
    users_favorite_posts = posts_model.FavoritePost.objects.filter(user = request.user)
    context = {
        "user_posts":users_posts,
        "user_comments":uesrs_comments,
        "user_favorite_posts":users_favorite_posts
        }
    if request.method == "POST" and request.POST.get("_method") == "DELETE":
        target_post = posts_model.Comment.objects.get(pk = request.POST.get("comment"))
        target_post.delete()
    return render(request,"users/users_info.html",context)

@login_required(login_url="/users/login")
def users_change_pass_view(request):
    context = {
        "change_pass_form":PasswordChangeForm(request.user or None)
    }
    return render(request,"users/users_change_pass.html",context)