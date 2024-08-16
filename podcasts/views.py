from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from .models import Podcast,PodcastComment
from .forms import PodcastCommentForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
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
def add_podcast(request):
    return HttpResponse('')