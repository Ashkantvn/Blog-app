from django.http import HttpResponse



def users_view(request):
    return HttpResponse("HELLO USER")