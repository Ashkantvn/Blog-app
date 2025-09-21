import pytest

@pytest.mark.django_db
class TestAccountModels:
    
    # The 'user' fixture is defined in conftest.py
    # Tests for the custom user model
    def test_create_user(self, user):
        assert user.username == "testuser"
        assert user.is_active
        assert user.profile_image is not None
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.check_password("testpassword123")
        assert user.user_slug == "testuser"
        assert hasattr(user, 'last_login')
        assert user.created_date is not None
        assert user.updated_date is not None
        assert not hasattr(user, 'email')
        assert not hasattr(user, 'is_staff')


    def test_user_str(self, user):
        assert str(user) == f"{user.first_name} {user.last_name}"