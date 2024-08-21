from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse,reverse_lazy
from .models import Podcast,PodcastComment
from .forms import PodcastCommentForm,PodcastForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

# podcast list view
def podcast_list(request):
    podcasts = Podcast.objects.all().order_by('-created_date')
    paginator = Paginator(podcasts,10)
    current_page = request.GET.get('page',1)
    try:
        paginator_result = paginator.page(current_page)
    except PageNotAnInteger:
        paginator_result = paginator.page(1)
    except EmptyPage:
        paginator_result = paginator.page(paginator.num_pages)
    context = {
        "podcasts":paginator_result
    }
    return render(request,'podcasts/podcasts_list.html',context)


#podcast details view
def podcast_details(request,pk):
    podcast = Podcast.objects.get(pk = pk)
    comments = PodcastComment.objects.filter(comment_for = podcast)
    form = PodcastCommentForm(request.POST or None)
    status_code = 200
    context={
        "podcast":podcast,
        'comments':comments,
        'form':form
    }
    if request.method=='POST':
        if request.user.is_authenticated :
            if form.is_valid():
                comment_form = form.save(commit=False)
                comment_form.author = request.user
                comment_form.comment_for = podcast
                comment_form.save()
                status_code = 201
        else:
            return redirect(reverse('users:login'))
        
    return render(request,'podcasts/podcasts_details.html',context,status=status_code)


#Add new podcast view
@login_required(login_url=reverse_lazy('users:login'))
def add_podcast(request):
    form = PodcastForm(request.POST or None , request.FILES)
    context = {
        'form':form
    }
    status_code = 200
    if request.method == "POST":
        if form.is_valid():
            podcast_form = form.save(commit=False)
            podcast_form.podcaster = request.user
            podcast_form.save()
            status_code = 201
            messages.success(request,"Successfully added")
        else:
            for field , errors in form.errors.items():
                for error in errors:
                    messages.error(request,f"{field} : {error}")
    return render(request,'podcasts/add_podcasts.html',context,status=status_code)


@login_required(login_url=reverse_lazy('users:login'))
def edit_podcast(request,pk):
    target_podcast = Podcast.objects.get(pk= pk)
    if request.method == 'POST':
        form = PodcastForm(request.POST,request.FILES, instance=target_podcast)
        if target_podcast.podcaster == request.user:
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully updated!')
        else:
            messages.error(request,"You can only edit your posts")
    else:
        form = PodcastForm(instance=target_podcast)
    
    context = {
        "podcast":target_podcast,
        "form":form
    }
    return render(request,'podcasts/edit_podcasts.html',context)



def delete_podcast(request,pk):
    return HttpResponse("")