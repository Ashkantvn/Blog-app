import pytest
from django.test import Client
from django.urls import reverse
from http import HTTPStatus
from accounts.models import ConfirmCode

@pytest.mark.django_db
class TestResetAndActivationViews:
    def setup_method(self):
        self.client = Client()
        self.password_reset_url = reverse("accounts:reset")

    # Password reset
    def test_GET_password_reset_200(self):
        response = self.client.get(self.password_reset_url)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "accounts/reset-and-activation/password_reset.html" in [
            template.name for template in response.templates
        ]

    def test_POST_password_reset_200(self,user):
        data = {
            "email": user.email,
        }
        response = self.client.post(self.password_reset_url,data)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "accounts/reset-and-activation/password_reset.html" in [
            template.name for template in response.templates
        ]

    def test_POST_password_reset_404(self):
        data = {
            "email": "someone@test.com",
        }
        response = self.client.post(self.password_reset_url,data)
        # Asserts
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context
        assert "accounts/reset-and-activation/password_reset.html" in [
            template.name for template in response.templates
        ]

    def test_POST_password_reset_400(self):
        data={
            "email": "sometihng",
        }
        response = self.client.post(self.password_reset_url,data)
        # Asserts
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "error" in response.context
        assert "accounts/reset-and-activation/password_reset.html" in [
            template.name for template in response.templates
        ]

    # Password reset confirm's tests
    def test_GET_password_reset_confirm_200(self, confirm_code):
        url = reverse("accounts:reset-confirm",args=[confirm_code.code])
        response = self.client.get(url)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "accounts/reset-and-activation/password_reset_confirm.html" in [
            template.name for template in response.templates
        ]
    
    def test_GET_password_reset_confirm_404(self):
        url = reverse("accounts:reset-confirm",args=["confirm_code.code"])
        response = self.client.get(url)
        # Asserts
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context
        assert "accounts/reset-and-activation/password_reset_confirm.html" in [
            template.name for template in response.templates
        ]

    def test_POST_password_reset_confirm_200(self, confirm_code):
        data= {
            "password":"oajeocwmoiowjd@#$1345234",
            "password_confirm":"oajeocwmoiowjd@#$1345234"
        }
        url = reverse("accounts:reset-confirm",args=[confirm_code.code])
        response = self.client.post(url,data)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.context
        assert "accounts/reset-and-activation/password_reset_confirm.html" in [
            template.name for template in response.templates
        ]

    def test_POST_password_reset_confirm_404(self):
        data= {
            "password":"oajeocwmoiowjd@#$1345234",
            "password_confirm":"oajeocwmoiowjd@#$1345234"
        }
        url = reverse("accounts:reset-confirm",args=["confirm_code.code"])
        response = self.client.post(url,data)
        # Asserts
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context
        assert "accounts/reset-and-activation/password_reset_confirm.html" in [
            template.name for template in response.templates
        ]
    
    def test_POST_password_reset_confirm_400(self,confirm_code):
        data= {
            "password":"oajeocwmoiowjd@#$1345234",
            "password_confirm":"oajeocwmoiowjd@#"
        }
        url = reverse("accounts:reset-confirm",args=[confirm_code.code])
        response = self.client.post(url,data)
        # Asserts
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "error" in response.context
        assert "accounts/reset-and-activation/password_reset_confirm.html" in [
            template.name for template in response.templates
        ]

    # Account activation tests
    def test_GET_activations_200(self,inactive_user):
        url = reverse("accounts:activate",args=[inactive_user.user_slug])
        response= self.client.get(url)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "accounts/reset-and-activation/activation.html" in [
            template.name for template in response.templates
        ]

    def test_GET_activations_404(self):
        url = reverse("accounts:activate",args=["inactive_user.user_slug"])
        response= self.client.get(url)
        # Asserts
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context
        assert "accounts/reset-and-activation/activation.html" in [
            template.name for template in response.templates
        ]

    def test_POST_activations_200(self,inactive_user):
        url = reverse("accounts:activate",args=[inactive_user.user_slug])
        confirm_code = ConfirmCode.objects.create(
            code = "lakjdofj2342",
            user= inactive_user
        )
        data={
            "code":confirm_code.code,
            "password":"testpassword1230",
        }
        response= self.client.post(url,data)
        # Asserts
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.context
        assert "accounts/reset-and-activation/activation.html" in [
            template.name for template in response.templates
        ]

    def test_POST_activations_403(self,inactive_user,confirm_code):
        url = reverse("accounts:activate",args=[inactive_user.user_slug])
        data={
            "code":confirm_code.code,
            "password":"testpasrd123",
        }
        response= self.client.post(url,data)
        # Asserts
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert "error" in response.context
        assert "accounts/reset-and-activation/activation.html" in [
            template.name for template in response.templates
        ]

    def test_POST_activations_404(self):
        url = reverse("accounts:activate",args=["inactive_user.user_slug"])
        data={
            "code":"confirm_code.code",
            "password":"testpasrd123",
        }
        response= self.client.post(url,data)
        # Asserts
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "error" in response.context
        assert "accounts/reset-and-activation/activation.html" in [
            template.name for template in response.templates
        ]