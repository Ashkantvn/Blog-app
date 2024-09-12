from django.urls import path
from . import views

app_name="photoGallery"
urlpatterns = [
    path("", views.gallery_view, name="list"),
    path("posts", views.post_gallery , name="posts"),
    path("podcasts", views.podcast_gallery, name="podcasts")
]
