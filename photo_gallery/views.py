from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post
# Create your views here.
def gallery_view(request):
    return render(request,'photo_gallery/list.html')


def post_gallery(request):
    posts = Post.objects.all()
    context = {
     'posts':posts   
    }
    return render(request,'photo_gallery/posts.html',context)