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
    if request.user.is_authenticated:
        favorite_posts = postModel.FavoritePost.objects.filter(user=request.user)[:9] 
    context = {
        "favorite_posts":favorite_posts,  
    }
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