import pytest
from django.urls import reverse, resolve
from core.views import Home


@pytest.mark.django_db
class TestCoreUrls:

    def test_home_page__url_is_resolved(self):
        url = reverse("home")
        view_class = resolve(url).func.view_class
        assert view_class == Home
