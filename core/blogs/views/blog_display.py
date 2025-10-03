from django.views import View
from blogs.models import Blog
from django.shortcuts import render
from http import HTTPStatus
from blogs.utils import render_blog_or_404
from django.utils.timezone import now

class BlogList(View):
    def get(self, request):
        tag = request.GET.get('q', '')
        blogs = Blog.objects.filter(
            is_published=True,
            publishable=True,
            published_date__lte=now().date()
        )
        # Filter blogs by tag if provided
        if tag:
            blogs = blogs.filter(
                tags__tag_name=tag,
            )
        return render(
            request,
            'blogs/blog-display/blog_list.html',
            {
                'data': blogs
            }
        )


class BlogDetails(View):
    def get(self, request, blog_slug):
        try:
            blog= Blog.objects.get(blog_slug=blog_slug)
            if (
            not blog.is_published or
            not blog.publishable or
            blog.published_date > now().date()
            ) and blog.author!=request.user:
                raise Blog.DoesNotExist
        except blog.DoesNotExist:
            return render(
                request,
                "blogs/blog-display/blog_details.html",
                {
                    "error":"blog not found!"
                },
                status=HTTPStatus.NOT_FOUND
            )
        return render(
            request,
            "blogs/blog-display/blog_details.html",
            {
                "data":blog
            },
        )
                