from django.shortcuts import render
from posts import models as postModel
from podcasts import models as podcastModel
from django.conf import settings
from django.utils import translation
from lingua import LanguageDetectorBuilder
from users.forms import ContactForm
from django.contrib import messages
from django.utils.timezone import now


def home_view(request):
    detector = LanguageDetectorBuilder.from_all_languages().build()
    latest_posts = postModel.Post.objects.filter(status=1,published_date__lt=now())[:9]
    comments = postModel.Comment.objects.all()[:9]
    latest_podcasts = podcastModel.Podcast.objects.all().order_by("-created_date")[:9]
    podcasts_comments = podcastModel.PodcastComment.objects.all().order_by("-created_date")[:9]

    for comment in comments:
        lang = detector.detect_language_of(comment.comment_for.content).iso_code_639_1.name.lower()
        comment.lang = lang

    for comment in podcasts_comments:
        lang = detector.detect_language_of(comment.comment_for.description).iso_code_639_1.name.lower()
        comment.lang = lang

    context = {
        "latest_posts":latest_posts,
        "comments":comments,  
        'latest_podcasts':latest_podcasts ,
        'podcasts_comments':podcasts_comments
    }
    if request.user.is_authenticated:
        favorite_posts = postModel.FavoritePost.objects.filter(user=request.user)[:9] 
        context["favorite_posts"] = favorite_posts
    return render(request,"home.html",context)



def about_view(request):
    return render(request,"about.html")



def change_lang_view(request):
    if request.method == "POST":
        user_language = request.POST.get('language')
        translation.activate(user_language)
        response = render(request,"setting.html")
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
    else:
        response = response = render(request,"setting.html")
    return response


def contact_view(request):
    form = ContactForm()
    context = {
        'form':form
    }
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                form_data = form.save(commit=False)
                form_data.user = request.user
                form_data.save()
            else:
                form.save()
            messages.add_message(request,messages.SUCCESS,"Your data submited successfully")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.add_message(request,messages.ERROR,f"{field}:{error}") 
                    
    return render(request,'contact.html',context)