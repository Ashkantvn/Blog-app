from django.contrib.syndication.views import Feed
from django.urls import reverse
from posts.models import Post

class LatestEntriesFeed(Feed):
    title = "Latest Posts"
    link = "/latest/feed/"
    description = "Latest blogs from BLOG."

    def items(self):
        return Post.objects.all()[:6]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:100]

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return item.get_absolute_url()
