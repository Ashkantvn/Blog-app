import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAccountModels:

    # The 'user' fixture is defined in conftest.py
    # Tests for the custom user model
    def test_create_user(self, user):

        assert user.username == "testuser"

        assert user.email == "test@example.com"

        assert user.first_name == "Test"

        assert user.last_name == "User"

        assert user.user_slug == "testuser"

        assert user.is_superuser is False, "User should not be a superuser"

        assert user.is_staff is False, "User should not be staff"

        assert user.is_active, "User is not active"

        assert user.check_password("testpassword123"), "Password check failed"

        assert hasattr(user, "profile_image"), \
            "User missing 'profile_image' attribute"

        assert hasattr(user, "last_login"), \
            "User missing 'last_login' attribute"

        assert hasattr(user, "created_date"), \
            "User missing 'created_date' attribute"

        assert hasattr(user, "updated_date"), \
            "User missing 'updated_date' attribute"

    def test_user_str(self, user):
        assert str(user) == f"{user.first_name} {user.last_name}"

    # The 'confirm_code' fixtrue is defined in conftest.py
    # Tests for confirm_code
    def test_create_confirm_code(self, confirm_code):
        assert confirm_code.code == "ladlfjlkajfl"

        assert isinstance(
            confirm_code.user, User
        ), "User is not an instance of User model"
        assert hasattr(confirm_code, "created_date"), \
            "Missing 'created_date' attribute"
        assert hasattr(confirm_code, "updated_date"), \
            "Missing 'updated_date' attribute"

    def test_confirm_code_str(self, confirm_code):
        assert str(confirm_code) == (
            f"{confirm_code.code} for {confirm_code.user.username}"
        )
