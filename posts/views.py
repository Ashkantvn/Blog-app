from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from . import models,forms
from django.contrib.auth.decorators import login_required

# Create your views here.
def posts_list_view(request):
    posts = models.Post.objects.all().order_by("-date_created")
    paginator = Paginator(posts,10)
    current_page = request.GET.get('page',1)
    try :# set ther current number of page in result and handle errors of inputs
        paginator_result = paginator.page(current_page)
    except PageNotAnInteger:
        paginator_result = paginator.page(1)
    except EmptyPage:
        paginator_result = paginator.page(paginator.num_pages)
    context = {"posts": paginator_result}   
    return render(request,'posts/posts_list.html',context)

def posts_details_view(request , pk):
    post = models.Post.objects.get(pk = pk)
    context = {"post" : post}
    return render(request,"posts/posts_details.html",context)

@login_required(login_url="/users/login")
def posts_add_view(request):
    if request.method == "POST":
        form = forms.AddPostForm(request.POST , request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("users:info")
    else :
        form = forms.AddPostForm()
    context = {"form":form}
    return render(request,"posts/posts_add.html",context)

def posts_edit_view(request):
    return HttpResponse("edit page")

def posts_delete_view(request):
    return HttpResponse ("delete page")