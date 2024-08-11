from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from . import views , models
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

# url tests
class testPodcastURL(SimpleTestCase):

    def test_podcast_list_is_resolve(self):
        url = reverse("podcasts:list")
        self.assertEqual(resolve(url).func,views.podcast_list)


# model tests

class testPodcastModels(TestCase):

    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username="testuser")[0])
        self.test_podcast = models.Podcast.objects.create(
            title = "Podcast title",
            description = "Something about podcast",
            audio = SimpleUploadedFile("test_audio.mp3",b'file_content','audio/mpeg'),
            podcaster = get_user(self.client)
        )

    def test_podcast_creation(self):
        self.assertEqual(self.test_podcast.title, "Podcast title")
        self.assertEqual(self.test_podcast.slug,"Podcast-title")
        self.assertEqual(self.test_podcast.podcaster, self.user)