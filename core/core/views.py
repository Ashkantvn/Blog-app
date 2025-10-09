from django.views import View
from django.shortcuts import render
from blogs.models import Blog
from django.utils.timezone import now


class Home(View):

    def get(self, request):
        blogs = Blog.objects.filter(
            is_published=True,
            publishable=True,
            published_date__lte=now().date()
        )
        latest_blogs = blogs.order_by("-published_date")
        most_view_blogs = blogs.order_by("-views")
        return render(
            request,
            "core/home.html",
            {
                "data": {
                    "latest_blogs": latest_blogs,
                    "most_view_blogs": most_view_blogs,
                },
            },
        )
