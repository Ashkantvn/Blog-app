from django.shortcuts import render,HttpResponse
from .models import Podcast

# Create your views here.

# podcast list view
def podcast_list(request):
    podcasts = Podcast.objects.all()
    context = {
        "podcasts":podcasts
    }
    return render(request,'podcasts/podcasts_list.html',context)