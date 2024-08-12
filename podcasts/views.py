from django.shortcuts import render,HttpResponse
from .models import Podcast
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.

# podcast list view
def podcast_list(request):
    podcasts = Podcast.objects.all()
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