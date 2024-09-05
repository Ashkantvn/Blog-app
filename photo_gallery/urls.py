from django.urls import path
from . import views

app_name="photoGallery"
urlpatterns = [
    path("", views.gallery_view, name="list")
]
