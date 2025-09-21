import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture(autouse=True)
def user():
    user_obj = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="testpassword123",
        is_active=True,
    )
    yield user_obj
    if user_obj.pk:
        user_obj.delete()
