import pytest
from django.contrib.auth import get_user_model
from accounts.models import ConfirmCode

User = get_user_model()

# User fixture
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

# Confrm code fixture
@pytest.fixture(autouse=True)
def confirm_code():
    user_obj = User.objects.create_user(
        username="testuser2",
        email="test2@example.com",
        first_name="Test2",
        last_name="User2",
        password="testpassword123",
        is_active=True,
    )
    confirm_code_obj = ConfirmCode.objects.create(
        code="ladlfjlkajfl",
        user=user_obj,
    )
    yield confirm_code_obj
    if confirm_code_obj.pk:
        confirm_code_obj.delete()