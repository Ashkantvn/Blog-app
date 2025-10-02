import pytest
from django.contrib.auth import get_user_model
from accounts.models import ConfirmCode
from django.test import Client
from blogs.models import Blog, Tag

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

# Inactive User fixture
@pytest.fixture(autouse=True)
def inactive_user():
    user_obj = User.objects.create_user(
        username="testuser30",
        email="test30@example.com",
        first_name="Test30",
        last_name="User30",
        password="testpassword1230",
        is_active=False,
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

# Authenticated user fixture
@pytest.fixture(autouse=True)
def authenticated_user():
    client = Client()
    user_obj = User.objects.create_user(
        username="testuser3",
        email="test3@example.com",
        first_name="Test3",
        last_name="User3",
        password="testpassword123",
        is_active=True,
    )
    blog_obj = Blog.objects.create(
        title="Test Blog Auth",
        content="This is a test blog content for authenticated user.",
        author=user_obj,
    )
    client.force_login(user_obj)
    client.blog = blog_obj
    yield client
    if user_obj.pk:
        user_obj.delete()

# Blog fixture
@pytest.fixture(autouse=True)
def blog():
    user = User.objects.create_user(
        username="testuser4",
        email="test4@test.com",
        first_name="Test4",
        last_name="User4",
        password="testpassword123",
        is_active=True,
    )
    blog_obj = Blog.objects.create(
        title="Test Blog",
        content="This is a test blog content.",
        author=user,
    )
    tag_obj = Tag.objects.create(
        tag_name="Test",
    )
    blog_obj.tags.add(tag_obj)
    yield blog_obj
    if user.pk:
        user.delete()

# Tag fixture
@pytest.fixture(autouse=True)
def tag():
    tag_obj = Tag.objects.create(
        tag_name="Django",
    )
    yield tag_obj
    if tag_obj.pk:
        tag_obj.delete()