import pytest
from django.urls import reverse
from django.test import Client
from http import HTTPStatus

@pytest.mark.django_db
class TestAccountAuthenticationViews:
    def setup_method(self):
        self.client = Client()
        self.login_url = reverse("accounts:login")
        self.signup_url = reverse("accounts:signup")
        self.logout_url = reverse("accounts:logout")

    # Login
    def test_GET_login_status_200(self):
        response = self.client.get(self.login_url)
        assert response.status_code == HTTPStatus.OK
        assert "accounts/authentications/login.html" in [
            template.name for template in response.templates
        ]

    def test_POST_login_status_200(self, user):
        data = {
            "email": user.email,
            "password": "testpassword123"
        }
        response = self.client.post(self.login_url,data)
        assert response.status_code == HTTPStatus.OK
        assert response.wsgi_request.user.is_authenticated , (
            "User is not authenticated"
        )
        assert "data" in response.context
        assert "accounts/authentications/login.html" in [
            template.name for template in response.templates
        ]

    def test_POST_login_status_404(self):
        data = {
            "email": "someone@email.com",
            "password": "soemogj@adoii2342@#$dlsjf"
        }
        response = self.client.post(self.login_url,data)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context
        assert "accounts/authentications/login.html" in [
            template.name for template in response.templates
        ]

    # Sign up
    def test_GET_sign_up_200(self):
        response = self.client.get(self.signup_url)
        assert response.status_code == HTTPStatus.OK
        assert "accounts/authentications/signup.html" in [
            template.name for template in response.templates
        ]

    def test_POST_sign_up_201(self):
        data = {
            "email": "test12345@test.com",
            "password": "oadf!@#@#$2345dsjflkj",
            "username": "testuser12345",
            "first_name": "Test",
        }
        response = self.client.post(self.signup_url,data)
        assert response.wsgi_request.user.is_authenticated , (
            "User is not authenticated"
        )
        assert response.status_code == HTTPStatus.CREATED
        assert "data" in response.context
        assert "accounts/authentications/signup.html" in [
            template.name for template in response.templates
        ]

    def test_POST_sign_up_400(self):
        data = {
            "email": "test12345m",
            "password": "oadf!@#@#$2345dsjflkj",
            "username": "testuser12345",
            "first_name": "Test",
        }
        response = self.client.post(self.signup_url,data)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "error" in response.context
        assert "accounts/authentications/signup.html" in [
            template.name for template in response.templates
        ]

    def test_POST_sign_up_403(self, user):
        data = {
            "email": user.email,
            "password": "oadf!@#@#$2345dsjflkj",
            "username": "testuser12345",
            "first_name": "Test",
        }
        response = self.client.post(self.signup_url,data)
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert "error" in response.context
        assert "accounts/authentications/signup.html" in [
            template.name for template in response.templates
        ]

    # Logout 
    def test_GET_logout_200(self, authenticated_user):
        client = authenticated_user
        response = client.get(self.logout_url)
        assert response.status_code == HTTPStatus.OK
        assert "accounts/authentications/logout.html" in [
            template.name for template in response.templates
        ]

    def test_GET_logout_401(self):
        response = self.client.get(self.logout_url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert "error" in response.context
        assert "accounts/authentications/logout.html" in [
            template.name for template in response.templates
        ]

    def test_POST_logout_200(self, authenticated_user):
        client = authenticated_user
        response = client.post(self.logout_url)
        assert response.status_code == HTTPStatus.OK
        assert not response.wsgi_request.user.is_authenticated , (
            "User is still authenticated"
        )
        assert "data" in response.context
        assert "accounts/authentications/logout.html" in [
            template.name for template in response.templates
        ]

    def test_POST_logout_401(self):
        response = self.client.post(self.logout_url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert "error" in response.context
        assert "accounts/authentications/logout.html" in [
            template.name for template in response.templates
        ]
