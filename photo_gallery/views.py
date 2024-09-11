from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post
from podcasts.models import Podcast
from django.utils.timezone import now
# Create your views here.
def gallery_view(request):
    return render(request,'photo_gallery/list.html')


def post_gallery(request):
    posts = Post.objects.filter(status=1,published_date__lt=now())
    context = {
     'posts':posts   
    }
    return render(request,'photo_gallery/posts.html',context)


def podcast_gallery(request):
    podcasts = Podcast.objects.all()
    context={
        'podcasts':podcasts
    }
    return render(request,'photo_gallery/podcasts.html',context)