from django.shortcuts import render
from posts import models





def home_view(request):
    latest_posts = models.Post.objects.all().order_by('-date_created')[:9]
    context = {"latest_posts":latest_posts}
    return render(request,"home.html",context)



def about_view(request):
    return render(request,"about.html")