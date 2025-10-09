from django.shortcuts import render
from http import HTTPStatus
from blogs.models import Blog


class AuthorRequiredMixin:
    template_name = (  # Default template for error rendering
        "blogs/blog-management/edit_blog.html"
    )

    def dispatch(self, request, *args, **kwargs):
        blog_slug = kwargs.get("blog_slug")
        # Fetch the blog post by slug
        try:
            blog = Blog.objects.get(blog_slug=blog_slug)
        except Blog.DoesNotExist:
            return render(
                request,
                self.template_name,
                {"error": "Blog not found"},
                status=HTTPStatus.NOT_FOUND,
            )
        # Check if the logged-in user is the author
        if blog.author != request.user:
            return render(
                request,
                self.template_name,
                {"error": "You are not authorized to edit this blog"},
                status=HTTPStatus.FORBIDDEN,
            )
        return super().dispatch(request, *args, **kwargs)
