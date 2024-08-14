from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from . import views , models ,forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

# url tests
class TestPodcastURL(SimpleTestCase):

    def test_podcast_list_is_resolve(self):
        url = reverse("podcasts:list")
        self.assertEqual(resolve(url).func,views.podcast_list)

    def test_podcast_details_is_resolve(self):
        url=reverse("podcasts:details",kwargs={"pk":1})
        self.assertEqual(resolve(url).func,views.podcast_details)


# model tests

class TestPodcastModels(TestCase):

    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username="testuser")[0])
        self.test_podcast = models.Podcast.objects.create(
            title = "Podcast title",
            description = "Something about podcast",
            audio = SimpleUploadedFile('test_audio.mp3',b'file_content','audio/mpeg'),
            podcaster = get_user(self.client)
        )

    def test_podcast_creation(self):
        self.assertEqual(self.test_podcast.title, "Podcast title")
        self.assertEqual(self.test_podcast.slug,"podcast-title")
        self.assertEqual(self.test_podcast.podcaster, get_user(self.client))


# form test 

class TestPodcastForms(SimpleTestCase):

    def test_podcast_form_with_valid_data(self):
        form = forms.PodcastForm(
            data={
                'title':'Title podcast',
                'description':'Podcast description',
            },
            files = {
                'audio':SimpleUploadedFile('test_audio.mp3',b'file_content','audio/mpeg')
            }
        )
        self.assertTrue(form.is_valid())

    def test_podcast_form_with_invalid_data(self):
        form = forms.PodcastForm(data={})
        self.assertFalse(form.is_valid())    




#views test (guest user)

class TestPodcastLoggedOutViews(TestCase):

    def test_logged_out_podcast_list_views(self):
        response = self.client.get(reverse("podcasts:list"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'podcasts/podcasts_list.html')