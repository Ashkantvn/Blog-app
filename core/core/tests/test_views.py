import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestCoreViews:

    def test_home_page_view(self):
        client = Client()
        url = reverse("home")
        response = client.get(url)
        assert response.status_code == 200
        assert "core/home.html" in [
            template.name for template in response.templates
        ]
