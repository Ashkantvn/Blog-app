import pytest
from django.urls import reverse, resolve
from blogs import views


@pytest.mark.django_db
class TestBlogURLs:
    def test_blog_list_is_resolved(self):
        url = reverse("blogs:list")
        view_class = resolve(url).func.view_class
        assert view_class == views.BlogList
        assert url == "/blogs/"

    def test_blog_details_is_resolved(self):
        url = reverse("blogs:details", kwargs={"blog_slug": "blog_slug"})
        view_class = resolve(url).func.view_class
        assert view_class == views.BlogDetails
        assert url == "/blogs/blog_slug/"

    def test_blog_add_is_resolved(self):
        url = reverse("blogs:add")
        view_class = resolve(url).func.view_class
        assert view_class == views.BlogAdd
        assert url == "/blogs/add/"

    def test_blog_edit_is_resolved(self):
        url = reverse("blogs:edit", kwargs={"blog_slug": "blog_slug"})
        view_class = resolve(url).func.view_class
        assert view_class == views.BlogEdit
        assert url == "/blogs/blog_slug/edit/"

    def test_blog_delete_is_resolved(self):
        url = reverse("blogs:delete", kwargs={"blog_slug": "blog_slug"})
        view_class = resolve(url).func.view_class
        assert view_class == views.BlogDelete
        assert url == "/blogs/blog_slug/delete/"
