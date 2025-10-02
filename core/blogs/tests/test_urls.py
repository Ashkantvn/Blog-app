import pytest
from django.urls import reverse, resolve
from blogs import views

@pytest.mark.django_db
class TestBlogURLs:
    def test_blog_details_is_resolved(self):
        url = reverse("blogs:details", kwargs={"blog_slug": "blog_slug"})
        view_class = resolve(url).func.view_class
        assert view_class == views.BlogDetails
        assert url == "/blogs/blog_slug/"