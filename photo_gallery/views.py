from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def gallery_view(request):
    return render(request,'photo_gallery/list.html')


def post_gallery(request):
    return render(request,'photo_gallery/posts.html')