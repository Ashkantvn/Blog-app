from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from http import HTTPStatus
from blogs.models import Blog, Tag
from blogs.utils import render_blog_or_404, handle_tags
from blogs.mixins import AuthorRequiredMixin
from django.utils.text import slugify

class BlogAdd(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            'blogs/blog-management/add_blog.html',
        )
    
    def post(self, request):
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        banner = request.FILES.get('banner', None)
        tags = request.POST.get('tags', '')  # Comma-separated tags
        is_published = request.POST.get('is_published', 'off') == 'on'
        published_date = request.POST.get('published_date', None)
        if not all([title, content]):
            return render(
                request,
                'blogs/blog-management/add_blog.html',
                {
                    'error': 'Title and Content are required.'
                },
                status=HTTPStatus.BAD_REQUEST
            )
        # Check if blog is exists
        if Blog.objects.filter(blog_slug=slugify(title)).exists():
            return render(
                request,
                'blogs/blog-management/add_blog.html',
                {
                    'error': 'Blog is exist.'
                },
                status=HTTPStatus.BAD_REQUEST
            )
        # Create the blog post
        blog_data = {
            'title': title,
            'content': content,
            'is_published': is_published,
            'author': request.user
        }
        # Handle banner if provided
        if published_date:
            blog_data['published_date'] = published_date
        if banner:
            blog_data['banner'] = banner
        created_blog = Blog.objects.create(**blog_data)
        # Handle tags
        handle_tags(created_blog, tags)
        return render(
            request,
            'blogs/blog-management/add_blog.html',
            {
                "data": "Blog created successfully!"
            },
            status=HTTPStatus.CREATED
        )

class BlogEdit(LoginRequiredMixin, AuthorRequiredMixin, View):
    template_name = 'blogs/blog-management/edit_blog.html'

    def get(self, request, blog_slug):
        template = 'blogs/blog-management/edit_blog.html'
        return render_blog_or_404(request,template,blog_slug)
    
    def post(self, request, blog_slug):
        try:
            blog = Blog.objects.get(blog_slug=blog_slug)
        except Blog.DoesNotExist:
            return render(
                request,
                'blogs/blog-management/edit_blog.html',
                {
                    'error': 'Blog not found'
                },
                status=HTTPStatus.NOT_FOUND
            )
        # Get form data
        title = request.POST.get('title', blog.title)
        content = request.POST.get('content', blog.content)
        banner = request.FILES.get('banner', None)
        tags = request.POST.get('tags', '')  # Comma-separated tags
        is_published = request.POST.get('is_published', 'off') == 'on'
        published_date = request.POST.get('published_date', blog.published_date)
        # Update fields
        blog.title = title
        blog.content = content
        if banner:
            blog.banner = banner
        blog.is_published = is_published
        blog.published_date = published_date
        blog.save()
        # Handle tags
        handle_tags(blog, tags)
        return render(
            request,
            'blogs/blog-management/edit_blog.html',
            {
                "data": "Blog updated successfully!"
            },
            status=HTTPStatus.OK
        )

class BlogDelete(LoginRequiredMixin, AuthorRequiredMixin, View):
    template_name = 'blogs/blog-management/delete_blog.html'

    def get(self, request, blog_slug):
        template = 'blogs/blog-management/delete_blog.html'
        return render_blog_or_404(request,template,blog_slug)
    
    def post(self, request, blog_slug):
        try:
            blog = Blog.objects.get(blog_slug=blog_slug)
        except Blog.DoesNotExist:
            return render(
                request,
                'blogs/blog-management/delete_blog.html',
                {
                    'error': 'Blog not found'
                },
                status=HTTPStatus.NOT_FOUND
            )
        blog.delete()
        return render(
            request,
            'blogs/blog-management/delete_blog.html',
            {
                "data": "Blog deleted successfully!"
            },
            status=HTTPStatus.OK
        )