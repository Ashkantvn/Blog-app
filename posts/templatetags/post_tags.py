from django import template
from posts.models import Post,Comment
from podcasts.models import PodcastComment
from django.utils.timezone import now
from lingua import LanguageDetectorBuilder

register = template.Library()


@register.inclusion_tag("tags/items.html")
def latest_posts():
    latest_posts = Post.objects.filter(status=1,published_date__lt=now())[:9]

    
    return {
        "targets": latest_posts,
    }

@register.inclusion_tag('tags/comments.html', takes_context=True)
def latest_comments(context):
    detector = LanguageDetectorBuilder.from_all_languages().build()
    comments = Comment.objects.all()[:9]
    podcasts_comments = PodcastComment.objects.all().order_by("-created_date")[:9]

    for comment in comments:
        lang = detector.detect_language_of(comment.comment_for.content).iso_code_639_1.name.lower()
        comment.lang = lang

    for comment in podcasts_comments:
        lang = detector.detect_language_of(comment.comment_for.description).iso_code_639_1.name.lower()
        comment.lang = lang
    
    return {
        "comments": comments,
        'podcasts_comments':podcasts_comments
        
    }

