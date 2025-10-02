from django.urls import path
from blogs.views import BlogDetails

app_name = 'blogs'

urlpatterns = [
    # Blog display
    path('<slug:blog_slug>/', BlogDetails.as_view(), name='details'),
]
