from django.urls import path
from . import views

app_name="posts"

urlpatterns = [
    path("",views.posts_list_view,name="list"),
    path("details/",views.posts_details_view,name="details"),
    path("edit/",views.posts_edit_view,name="edit"),
    path("add/",views.posts_add_view,name="add"),
    path("delete/",views.posts_delete_view,name="delete"),
]
