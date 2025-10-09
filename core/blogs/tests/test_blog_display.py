import pytest
from django.test import Client
from django.urls import reverse
from http import HTTPStatus


@pytest.mark.django_db
class TestBlogDisplayViews:
    def setup_method(self):
        self.client = Client()

    # Blog List View Tests
    def test_GET_blog_list_view_200(self):
        url = reverse("blogs:list")
        response = self.client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.context, "Does not have data field"
        assert "blogs/blog-display/blog_list.html" in [
            template.name for template in response.templates
        ]

    def test_GET_blog_list_view_with_search_query_200(self, blog):
        blog_tag = blog.tags.first().tag_name
        url = reverse("blogs:list") + f"?q={blog_tag}"
        response = self.client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.context, "Does not have data field"
        assert "blogs/blog-display/blog_list.html" in [
            template.name for template in response.templates
        ]

    # Blog Detail View Tests
    def test_GET_blog_detail_view_200(self, blog):
        url = reverse("blogs:details", kwargs={"blog_slug": blog.blog_slug})
        response = self.client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.context, "Does not have data field"
        assert "blogs/blog-display/blog_details.html" in [
            template.name for template in response.templates
        ]
        # check view count increment
        blog.refresh_from_db()
        assert blog.views == 1

    def test_GET_blog_detail_view_404(self):
        url = reverse(
            "blogs:details",
            kwargs={"blog_slug": "non-existent-slug"}
        )
        response = self.client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context, "Does not have error field"
        assert "blogs/blog-display/blog_details.html" in [
            template.name for template in response.templates
        ]
