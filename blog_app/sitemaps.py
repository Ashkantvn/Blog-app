from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from posts.models import Post
from podcasts.models import Podcast

class StaticViewSiteMap(Sitemap):
    priority = 0.5
    changefreq = 'daily'



    def items(self):
        return ['about','home','posts:list','podcasts:list','users:info','posts:add','podcasts:add','users:login','users:register','users:logout','users:change-pass']
    
    def location(self,item):
        return reverse(item)


class PodcastsViewSiteMap(Sitemap):
    priority=0.5
    changefreq = 'never'

    def items(self):
        return Podcast.objects.all()
    
    def lastmod(self,obj):
        return obj.created_date
    



class PostsViewSiteMap(Sitemap):
    priority=0.5
    changefreq = 'never'

    def items(self):
        return Post.objects.all()
    
    def lastmod(self,obj):
        return obj.date_created