from django.shortcuts import render,HttpResponse

# Create your views here.

# podcast list view
def podcast_list(request):
    return HttpResponse("PODCAST")