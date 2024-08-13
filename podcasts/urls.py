from django.urls import path
from . import views

app_name="podcasts"

urlpatterns = [
    path("",views.podcast_list,name="list"),
    path('<int:pk>/',views.podcast_details,name="details")
]
