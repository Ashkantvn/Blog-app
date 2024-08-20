from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,PasswordChangeForm
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,update_session_auth_hash
from posts import models as posts_model
from django.contrib import messages
from lingua import LanguageDetectorBuilder
from django.urls import reverse

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
    detector = LanguageDetectorBuilder.from_all_languages().build()
    users_posts = posts_model.Post.objects.filter(author = request.user)
    uesrs_comments = posts_model.Comment.objects.filter(author = request.user)
    users_favorite_posts = posts_model.FavoritePost.objects.filter(user = request.user)
    for post in users_posts:
        lang = detector.detect_language_of(post.content).iso_code_639_1.name.lower()
        post.lang = lang
    for comment in uesrs_comments:
        lang = detector.detect_language_of(comment.content).iso_code_639_1.name.lower()
        comment.lang = lang
    context = {
        "user_posts":users_posts,
        "user_comments":uesrs_comments,
        "user_favorite_posts":users_favorite_posts
        }
    if request.method == "POST" and request.POST.get("_method") == "DELETE":
        target_comment = posts_model.Comment.objects.get(pk = request.POST.get("comment"))
        target_comment.delete()
        return redirect(reverse('users:info'))
    
    return render(request,"users/users_info.html",context)



@login_required(login_url="/users/login")
def users_change_pass_view(request): # will update and change user's password
    pass_change_form = PasswordChangeForm(request.user,request.POST or None)
    context = {
        "change_pass_form":pass_change_form
    }
    
    if request.method == "POST" and pass_change_form.is_valid():
        pass_change_form.save()
        update_session_auth_hash(request,pass_change_form.user)
        messages.success(request,"pass changed successfully")

    return render(request,"users/users_change_pass.html",context)