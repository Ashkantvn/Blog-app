from blogs.models import Blog
from http import HTTPStatus
from django.shortcuts import render


def render_blog_or_404(request, template, blog_slug):
    # Fetch the blog post by slug
    try:
        blog = Blog.objects.get(blog_slug=blog_slug)
    except Blog.DoesNotExist:
        return render(
            request,
            template,
            {"error": "Blog not found"},
            status=HTTPStatus.NOT_FOUND
        )
    # Render the blog details
    return render(request, template, {"data": blog})
