from blogs.models import Blog
from http import HTTPStatus
from django.shortcuts import render

def render_blog_or_404(request,template,blog_slug,view_increment=False):
    # Fetch the blog post by slug
    try:
        blog = Blog.objects.get(blog_slug=blog_slug)
    except Blog.DoesNotExist:
        return render(
            request,
            template,
            {
                'error': 'Blog not found'
            },
            status=HTTPStatus.NOT_FOUND
        )
    # Increment view count if specified
    if view_increment:
        blog.views += 1
        blog.save()
    # Render the blog details
    return render(
        request,
        template,
        {
            'data': blog
        }
    )