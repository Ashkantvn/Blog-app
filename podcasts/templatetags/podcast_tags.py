from django import template
from podcasts.models import Podcast

register = template.Library()


@register.inclusion_tag("tags/items.html")
def latest_podcasts():
    latest_podcasts = Podcast.objects.all()[:9]
    
    return {
        "targets": latest_podcasts,
        'is_podcast':True
    }


