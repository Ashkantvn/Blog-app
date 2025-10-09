from django.urls import path
from blogs.views import BlogDetails, BlogList, BlogAdd, BlogEdit, BlogDelete

app_name = "blogs"

urlpatterns = [
    # Blog display (list)
    path("", BlogList.as_view(), name="list"),
    # Blog management (add)
    path("add/", BlogAdd.as_view(), name="add"),
    # Blog display (details)
    path("<slug:blog_slug>/", BlogDetails.as_view(), name="details"),
    # Blog management (edit and delete)
    path("<slug:blog_slug>/edit/", BlogEdit.as_view(), name="edit"),
    path("<slug:blog_slug>/delete/", BlogDelete.as_view(), name="delete"),
]
