import pytest
from django.test import Client
from django.urls import reverse
from http import HTTPStatus
from blogs.models import Blog

@pytest.mark.django_db
class TestBlogManagementViews:
    def setup_method(self):
        self.client = Client()
        self.blog_data = {
            "title": "Sample Blog Title",
            "content": "This is a sample blog content.",
        }
        self.blog_update_data = {
            "title": "Updated Blog Title",
            "content": "This is the updated blog content.",
        }
    
    # Add blog view tests
    def test_GET_add_blog_view_200(self, authenticated_user):
        url = reverse("blogs:add")
        response = authenticated_user.get(url)
        assert response.status_code == HTTPStatus.OK
        assert "blogs/blog-management/add_blog.html" in [
            template.name for template in response.templates
        ]

    def test_GET_add_blog_view_302(self):
        url = reverse("blogs:add")
        response = self.client.get(url)
        assert response.status_code == HTTPStatus.FOUND  
        assert response.url.startswith(reverse("accounts:login")),(
            "response url is not started with login page"
        )

    def test_POST_add_blog_view_302(self):
        url = reverse("blogs:add")
        response = self.client.post(url, self.blog_data)
        assert response.status_code == HTTPStatus.FOUND  
        assert response.url.startswith(reverse("accounts:login")),(
            "response url is not started with login page"
        )

    def test_POST_add_blog_view_201(self, authenticated_user):
        url = reverse("blogs:add")
        response = authenticated_user.post(url, self.blog_data)
        assert response.status_code == HTTPStatus.CREATED
        assert "data" in response.context,(
            "data field does not exist"
        )
        assert "blogs/blog-management/add_blog.html" in [
            template.name for template in response.templates
        ]

    def test_POST_add_blog_view_400(self, authenticated_user):
        url = reverse("blogs:add")
        data = {
            "title": "",  
            "content": "This is the content of the new blog post.",
        }
        response = authenticated_user.post(url, data)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "error" in response.context,(
            "Does not have error field"
        )
        assert "blogs/blog-management/add_blog.html" in [
            template.name for template in response.templates
        ]

    # Edit blog view tests
    def test_GET_edit_blog_view_200(self, authenticated_user):
        blog = authenticated_user.blog
        url = reverse("blogs:edit", kwargs={"blog_slug": blog.blog_slug})
        response = authenticated_user.get(url)
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.context,(
            "data field does not exist"
        )
        assert "blogs/blog-management/edit_blog.html" in [
            template.name for template in response.templates
        ]

    def test_GET_edit_blog_view_404(self, authenticated_user):
        url = reverse("blogs:edit", kwargs={"blog_slug": "non-existent-slug"})
        response = authenticated_user.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context,(
            "Does not have error field"
        )
        assert "blogs/blog-management/edit_blog.html" in [
            template.name for template in response.templates
        ]

    def test_GET_edit_blog_view_403(self, authenticated_user, blog):
        url = reverse("blogs:edit", kwargs={"blog_slug": blog.blog_slug})
        response = authenticated_user.get(url)
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert "error" in response.context,(
            "Does not have error field"
        )
        assert "blogs/blog-management/edit_blog.html" in [
            template.name for template in response.templates
        ]
    
    def test_GET_edit_blog_view_302(self,blog):
        url = reverse("blogs:edit", kwargs={"blog_slug": blog.blog_slug})
        response = self.client.get(url)
        assert response.status_code == HTTPStatus.FOUND  
        assert response.url.startswith(reverse("accounts:login")),(
            "response url is not started with login page"
        )

    def test_POST_edit_blog_view_302(self,blog):
        url = reverse("blogs:edit", kwargs={"blog_slug": blog.blog_slug})
        response = self.client.post(url, self.blog_data)
        assert response.status_code == HTTPStatus.FOUND  
        assert response.url.startswith(reverse("accounts:login")),(
            "response url is not started with login page"
        )

    def test_POST_edit_blog_view_200(self, authenticated_user):
        blog = authenticated_user.blog
        url = reverse("blogs:edit", kwargs={"blog_slug": blog.blog_slug})
        response = authenticated_user.post(url, self.blog_update_data)
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.context,(
            "data field does not exist"
        )
        assert "blogs/blog-management/edit_blog.html" in [
            template.name for template in response.templates
        ]
        # Verify the blog was updated
        blog.refresh_from_db()
        assert blog.title == self.blog_update_data["title"]
        assert blog.content == self.blog_update_data["content"]
    
    def test_POST_edit_blog_view_403(self, authenticated_user, blog):
        url = reverse("blogs:edit", kwargs={"blog_slug": blog.blog_slug})
        response = authenticated_user.post(url, self.blog_update_data)
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert "error" in response.context,(
            "Does not have error field"
        )
        assert "blogs/blog-management/edit_blog.html" in [
            template.name for template in response.templates
        ]

    def test_POST_edit_blog_view_404(self, authenticated_user):
        url = reverse("blogs:edit", kwargs={"blog_slug": "non-existent-slug"})
        response = authenticated_user.post(url, self.blog_update_data)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context,(
            "Does not have error field"
        )
        assert "blogs/blog-management/edit_blog.html" in [
            template.name for template in response.templates
        ]

    # Delete blog view tests
    def test_GET_delete_blog_view_200(self, authenticated_user):
        blog = authenticated_user.blog
        url = reverse("blogs:delete", kwargs={"blog_slug": blog.blog_slug})
        response = authenticated_user.get(url)
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.context,(
            "data field does not exist"
        )
        assert "blogs/blog-management/delete_blog.html" in [
            template.name for template in response.templates
        ]

    def test_GET_delete_blog_view_404(self, authenticated_user):
        url = reverse("blogs:delete", kwargs={"blog_slug": "non-existent-slug"})
        response = authenticated_user.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context,(
            "Does not have error field"
        )
        assert "blogs/blog-management/delete_blog.html" in [
            template.name for template in response.templates
        ]
    
    def test_GET_delete_blog_view_403(self, authenticated_user, blog):
        url = reverse("blogs:delete", kwargs={"blog_slug": blog.blog_slug})
        response = authenticated_user.get(url)
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert "error" in response.context,(
            "Does not have error field"
        )
        assert "blogs/blog-management/delete_blog.html" in [
            template.name for template in response.templates
        ]

    def test_GET_delete_blog_view_302(self,blog):
        url = reverse("blogs:delete", kwargs={"blog_slug": blog.blog_slug})
        response = self.client.get(url)
        assert response.status_code == HTTPStatus.FOUND  
        assert response.url.startswith(reverse("accounts:login")),(
            "response url is not started with login page"
        )

    def test_POST_delete_blog_view_302(self,blog):
        url = reverse("blogs:delete", kwargs={"blog_slug": blog.blog_slug})
        response = self.client.post(url)
        assert response.status_code == HTTPStatus.FOUND  
        assert response.url.startswith(reverse("accounts:login")),(
            "response url is not started with login page"
        )

    def test_POST_delete_blog_view_204(self, authenticated_user):
        blog = authenticated_user.blog
        url = reverse("blogs:delete", kwargs={"blog_slug": blog.blog_slug})
        response = authenticated_user.post(url)
        assert response.status_code == HTTPStatus.NO_CONTENT
        # Verify the blog was deleted
        is_exists = Blog.objects.filter(pk=blog.pk).exists()
        assert not is_exists, (
            "Blog was not deleted from the database"
        )

    def test_POST_delete_blog_view_403(self, authenticated_user, blog):
        url = reverse("blogs:delete", kwargs={"blog_slug": blog.blog_slug})
        response = authenticated_user.post(url)
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert "error" in response.context,(
            "Does not have error field"
        )
        assert "blogs/blog-management/delete_blog.html" in [
            template.name for template in response.templates
        ]

    def test_POST_delete_blog_view_404(self, authenticated_user):
        url = reverse("blogs:delete", kwargs={"blog_slug": "non-existent-slug"})
        response = authenticated_user.post(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context,(
            "Does not have error field"
        )
        assert "blogs/blog-management/delete_blog.html" in [
            template.name for template in response.templates
        ]
