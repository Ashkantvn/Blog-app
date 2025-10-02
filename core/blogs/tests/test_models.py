import pytest
from django.contrib.auth import get_user_model
from blogs.models import Tag

User = get_user_model()

@pytest.mark.django_db
class TestblogModel:
    def test_blog_creation(self, blog):
        assert blog.title == "Test Blog"
        assert blog.content == "This is a test blog content."
        assert blog.banner == "blogs/default.png"
        assert blog.views == 0
        assert isinstance(blog.tags.first(), Tag),(
            "tags is not a Tag instance"
        )
        assert blog.is_published is False,(
            "is_published should be False by default"
        )
        assert blog.publishable is False,(
            "publishable should be False by default"
        )
        assert isinstance(blog.author, User),(
            "author is not a User instance"
        )
        assert blog.blog_slug == "test-blog"
        assert blog.created_date is not None,(
            "created_date is not set"    
        )
        assert blog.updated_date is not None,(
            "updated_date is not set"
        )



    def test_blog_str(self, blog):
        assert str(blog) == f"{blog.title} by {blog.author.username}"

    def test_blog_get_absolute_url(self, blog):
        url = blog.get_absolute_url()
        assert url == f"/blogs/{blog.blog_slug}/"


@pytest.mark.django_db
class TestTagModel:
    def test_tag_creation(self, tag):
        assert tag.tag_name == "Django"
        assert tag.tag_slug == "django"
        assert tag.created_date is not None,(
            "created_date is not set"
        )
        assert tag.updated_date is not None,(
            "updated_date is not set"    
        )


    def test_tag_str(self, tag):
        assert str(tag) == tag.tag_name