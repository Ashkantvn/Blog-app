from blogs.models import Tag
from django.utils.text import slugify


def handle_tags(blog_instance, tags):
    if tags:
        blog_instance.tags.clear()
        tag_list = [tag.strip() for tag in tags.split(",")]
        for tag_name in tag_list:
            tag_obj = Tag.objects.get_or_create(
                tag_slug=slugify(tag_name), defaults={"tag_name": tag_name}
            )[0]
            tag_obj.tag_name = tag_name
            tag_obj.save()
            blog_instance.tags.add(tag_obj)
