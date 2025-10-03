from django.views import View
from blogs.models import Blog
from django.shortcuts import render
from http import HTTPStatus
from blogs.utils import render_blog_or_404

class BlogList(View):
    def get(self, request):
        tag = request.GET.get('q', '')
        # Filter blogs by tag if provided
        if tag:
            blogs = Blog.objects.filter(tags__tag_name=tag)
        else:
            blogs = Blog.objects.all()
        return render(
            request,
            'blogs/blog-display/blog_list.html',
            {
                'data': blogs
            }
        )


class BlogDetails(View):
    def get(self, request, blog_slug):
        template = 'blogs/blog-display/blog_details.html'
        return render_blog_or_404(
            request,
            template,
            blog_slug,
            view_increment=True
        )