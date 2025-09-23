import pytest
from django.urls import resolve, reverse
from accounts import views

@pytest.mark.django_db
class TestAccountsUrl:

    def test_profile_is_resolved(self):
        url= reverse("accounts:profile",args=["testuser"])
        view_class = resolve(url).func.view_class
        assert view_class == views.Profile

    def test_update_account_is_resolved(self):
        url= reverse("accounts:update")
        view_class = resolve(url).func.view_class
        assert view_class == views.UpdateAccount

    def test_delete_account_is_resolved(self):
        url= reverse("accounts:delete")
        view_class = resolve(url).func.view_class
        assert view_class == views.DeleteAccount

    def test_signup_is_resolved(self):
        url= reverse("accounts:signup")
        view_class = resolve(url).func.view_class
        assert view_class == views.SignUp

    def test_login_is_resolved(self):
        url= reverse("accounts:login")
        view_class = resolve(url).func.view_class
        assert view_class == views.Login

    def test_logout_is_resolved(self):
        url= reverse("accounts:logout")
        view_class = resolve(url).func.view_class
        assert view_class == views.Logout

    def test_password_reset_is_resolved(self):
        url= reverse("accounts:reset")
        view_class = resolve(url).func.view_class
        assert view_class == views.PasswordReset
    
    def test_password_reset_confirm_is_resolved(self):
        url= reverse("accounts:reset-confirm",args=["testcode"])
        view_class = resolve(url).func.view_class
        assert view_class == views.PasswordResetConfirm

    def test_activate_account_is_resolved(self):
        url= reverse("accounts:activate")
        view_class = resolve(url).func.view_class
        assert view_class == views.Activate

