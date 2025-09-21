import pytest

@pytest.mark.django_db
class TestAccountModels:
    
    # The 'user' fixture is defined in conftest.py
    # Tests for the custom user model
    def test_create_user(self, user):
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_superuser is False
        assert user.is_staff is False
        assert user.is_active
        assert user.check_password("testpassword123")
        assert hasattr(user, 'profile_image')
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.user_slug == "testuser"
        assert hasattr(user, 'last_login')
        assert hasattr(user, 'created_time')
        assert hasattr(user, 'updated_time')

    def test_user_str(self, user):
        assert str(user) == f"{user.first_name} {user.last_name}"