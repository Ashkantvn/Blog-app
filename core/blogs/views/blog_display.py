from django.views import View
from blogs.models import Blog
from django.shortcuts import render
from http import HTTPStatus

class BlogList(View):
    pass

class BlogDetails(View):
    
    def get(self, request, blog_slug):
        try:
            blog = Blog.objects.get(blog_slug=blog_slug)
            blog.views += 1
            blog.save()
            return render(
                request,
                'blogs/blog-display/blog_details.html',
                {'data': blog}
            )
        except Blog.DoesNotExist:
            return render(
                request,
                'blogs/blog-display/blog_details.html',
                {'error': 'Blog not found'},
                status=HTTPStatus.NOT_FOUND
            )