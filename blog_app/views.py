from django.shortcuts import render
from posts import models
from django.conf import settings
from django.utils import translation





def home_view(request):
    latest_posts = models.Post.objects.all().order_by('-date_created')[:9]
    comments = models.Comment.objects.all().order_by("-created_date")[:9]
    context = {
        "latest_posts":latest_posts,
        "comments":comments,   
    }
    if request.user.is_authenticated:
        favorite_posts = models.FavoritePost.objects.filter(user=request.user)[:9] 
        context["favorite_posts"] = favorite_posts
    return render(request,"home.html",context)



def about_view(request):
    return render(request,"about.html")



def change_lang_view(request):
    if request.method == "POST":
        user_language = request.POST.get('language')
        translation.activate(user_language)
        response = render(request,"setting.html")
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
    else:
        response = response = render(request,"setting.html")
    return response