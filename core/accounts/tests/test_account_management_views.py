import pytest
from django.test import Client
from django.urls import reverse
from http import HTTPStatus

@pytest.mark.django_db
class TestAccountManagementViews:
    def setup_method(self):
        self.client = Client()
        self.delete_url = reverse("accounts:delete")
        # Update data
        self.update_url = reverse("accounts:update")
        self.update_data={
            "password": "wodjafmpodjw@#334808"
        }

    # Profile tests
    def test_GET_profile_status_200(self,user):
        url = reverse("accounts:profile",args=[user.user_slug])
        response = self.client.get(url)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "accounts/account-management/profile.html" in [
            template.name for template in response.templates
        ]

    def test_GET_profile_status_404(self):
        url = reverse("accounts:profile",args=["user_slug"])
        response = self.client.get(url)
        # Asserts
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context
        assert "accounts/account-management/profile.html" in [
            template.name for template in response.templates
        ]

    # Account Update tests
    def test_GET_account_update_200(self, authenticated_user):
        client = authenticated_user
        response = client.get(self.update_url)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "accounts/account-management/update.html" in [
            template.name for template in response.templates
        ]

    def test_GET_account_update_401(self):
        response = self.client.get(self.update_url)
        # Asserts
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert "error" in response.context
        assert "accounts/account-management/update.html" in [
            template.name for template in response.templates
        ]

    def test_POST_account_update_200(self, authenticated_user):
        client = authenticated_user
        response = client.post(self.update_url,self.update_data)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.context
        assert "accounts/account-management/update.html" in [
            template.name for template in response.templates
        ]

    def test_POST_account_update_401(self):
        response = self.client.post(self.update_url,self.update_data)
        # Asserts
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert "error" in response.context
        assert "accounts/account-management/update.html" in [
            template.name for template in response.templates
        ]

    def test_POST_account_update_400(self, authenticated_user):
        client = authenticated_user
        data={
            "email":"something"
        }
        response = client.post(self.update_url,data)
        # Asserts
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "error" in response.context
        assert "accounts/account-management/update.html" in [
            template.name for template in response.templates
        ]


    # Delete Account tests
    def test_GET_delete_account_200(self, authenticated_user):
        client = authenticated_user
        response = client.get(self.delete_url)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "accounts/account-managemet/delete.html" in [
            template.name for template in response.templates
        ]
    
    def test_GET_delete_account_401(self):
        response = self.client.get(self.delete_url)
        # Asserts
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert "error" in response.context
        assert "accounts/account-managemet/delete.html" in [
            template.name for template in response.templates
        ]

    def test_POST_delete_account_200(self, authenticated_user):
        client = authenticated_user
        response = client.post(self.delete_url)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.context
        assert "accounts/account-managemet/delete.html" in [
            template.name for template in response.templates
        ]

    def test_POST_delete_account_401(self):
        response = self.client.post(self.delete_url)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "error" in response.context
        assert "accounts/account-managemet/delete.html" in [
            template.name for template in response.templates
        ]