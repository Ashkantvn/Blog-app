from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from . import views

# Create your tests here.

# url tests
class testPodcastURL(SimpleTestCase):

    def test_podcast_list_is_resolve(self):
        url = reverse("podcasts:list")
        self.assertEqual(resolve(url).func,views.podcast_list)