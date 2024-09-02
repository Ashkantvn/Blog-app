from django.shortcuts import render , redirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from . import models,forms
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from lingua import LanguageDetectorBuilder
from django.contrib.messages import success

# Create your views here.
def posts_list_view(request):
    posts = models.Post.objects.all()
    paginator = Paginator(posts,10)
    current_page = request.GET.get('page',1)
    try :# set the current page in paginator result to do pagination of blogs(posts) and handle errors of inputs 
        paginator_result = paginator.page(current_page)
    except PageNotAnInteger:
        paginator_result = paginator.page(1)
    except EmptyPage:
        paginator_result = paginator.page(paginator.num_pages)# set the last page if page was empty
    context = {"posts": paginator_result}   
    return render(request,'posts/posts_list.html',context)

def posts_details_view(request , pk):
    post = models.Post.objects.get(pk = pk)
    form = forms.CommentsForm(request.POST or None)
    comments = models.Comment.objects.filter(comment_for = post)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(reverse("users:login"))
        elif request.POST.get("favorite_post"):
            if not models.FavoritePost.objects.filter(post = post,user=request.user):
                favorite_post = models.FavoritePost.objects.create(
                    post = post,
                    user = request.user
                )
                favorite_post.save()
            return redirect(reverse("users:info"))
        else:
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.comment_for = post
                new_comment.save()

    context = {
        "post" : post,
        "form" : form,
        "comments":comments
    }
    return render(request,"posts/posts_details.html",context)

@login_required(login_url=reverse_lazy("users:login"))
def posts_add_view(request):
    if request.method == "POST":
        form = forms.PostForm(request.POST , request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("users:info")
    else :
        form = forms.PostForm()
    context = {"form":form}
    return render(request,"posts/posts_add.html",context)


@login_required(login_url=reverse_lazy("users:login"))
def posts_edit_view(request,pk):
    user_post = models.Post.objects.get(pk = pk)
    detector = LanguageDetectorBuilder.from_all_languages().build()

    #language detector
    lang = detector.detect_language_of(user_post.content).iso_code_639_1.name.lower()
    user_post.lang = lang
    
    form = forms.PostForm(request.POST or None, request.FILES or None, instance=user_post)
    if request.method == "POST" and request.POST.get('_method')=="PUT":# check mehtod is PUT and target is exist
        if request.user == user_post.author and form.is_valid():
            form.save()
            success(request,"Post Changed")

    context = {
        "post":user_post,
        "form":form
    }
    return render(request,"posts/posts_edit.html",context)

@login_required(login_url=reverse_lazy("users:login"))
def posts_delete_view(request,pk):
    target_post = models.Post.objects.get(pk=pk)
    if request.method == "POST" and request.POST.get('_method') == "DELETE":
        if request.user == target_post.author and target_post:
            target_post.delete()
            return redirect(reverse("users:info"))
    context = {
        "post": target_post
    }
    return render(request,"posts/posts_delete.html",context)