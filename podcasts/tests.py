from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from . import views , models ,forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.translation import activate

# Create your tests here.

# url tests
class TestPodcastURL(SimpleTestCase):

    def test_podcast_list_is_resolve(self):
        url = reverse("podcasts:list")
        self.assertEqual(resolve(url).func,views.podcast_list)

    def test_podcast_details_is_resolve(self):
        url=reverse("podcasts:details",kwargs={"pk":1})
        self.assertEqual(resolve(url).func,views.podcast_details)

    def test_add_podcast_is_resolve(self):
        url = reverse('podcasts:add')
        self.assertEqual(resolve(url).func,views.add_podcast)

    def test_edit_podcast_is_resolve(self):
        url = reverse('podcasts:edit')
        self.assertEqual(resolve(url).func,views.edit_podcast)


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
        self.test_comment = models.PodcastComment.objects.create(
            content = 'test comment',
            comment_for = self.test_podcast,
            author = get_user(self.client)
        )

    def test_podcast_creation(self):
        self.assertEqual(self.test_podcast.title, "Podcast title")
        self.assertEqual(self.test_podcast.slug,"podcast-title")
        self.assertEqual(self.test_podcast.podcaster, get_user(self.client))

    def test_podcast_comment_creation(self):
        self.assertEqual(self.test_comment.content,'test comment')



# form test 

class TestPodcastForms(TestCase):

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

    def test_podcast_comment_form_with_valid_data(self):
        form = forms.PodcastCommentForm(
            data={
                'content':'test comment'
            }
        )
        self.assertTrue(form.is_valid())   

    def test_podcast_comment_form_with_invalid_data(self):
        form = forms.PodcastCommentForm(data={})
        self.assertFalse(form.is_valid())


#views test (guest user)

class TestPodcastLoggedOutViews(TestCase):

    def setUp(self):
        self.user = User.objects.update_or_create(username = "testuser")[0]
        self.test_podcast = models.Podcast.objects.create(
            title = "Podcast title",
            description = "Something about podcast",
            audio = SimpleUploadedFile('test_audio.mp3',b'file_content','audio/mpeg'),
            podcaster = self.user
        )

    def test_logged_out_podcast_list_views(self):
        response = self.client.get(reverse("podcasts:list"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'podcasts/podcasts_list.html')

    def test_logged_out_podcast_details_view(self):
        response = self.client.get(reverse("podcasts:details",kwargs={"pk":self.test_podcast.pk}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'podcasts/podcasts_details.html')

    def test_logged_out_podcast_details_POST_view(self):
        response = self.client.post(
            reverse("podcasts:details",kwargs={"pk":self.test_podcast.pk}),
            data={
                'content':"test comment",
            }
        )
        self.assertRedirects(response,reverse('users:login'))
    
    def test_logged_out_add_podcast_view(self):
        response = self.client.get(reverse('podcasts:add'))
        self.assertRedirects(response,f'{reverse('users:login')}?next={reverse('podcasts:add')}')

    def test_logged_out_add_podcast_POST_view(self):
        response = self.client.post(reverse('podcasts:add'),data={})
        self.assertRedirects(response,f'{reverse('users:login')}?next={reverse('podcasts:add')}')

    def test_logged_out_edit_podcast_view(self):
        response = self.client.get(reverse('podcasts:edit'))
        self.assertRedirects(response,f'{reverse('users:login')}?next={reverse("podcast:edit")}')
        
    def test_logged_out_edit_podcast_POST_view(self):
        response = self.client.post(reverse('podcasts:edit'),data={})
        self.assertRedirects(response,f'{reverse('users:login')}?next={reverse("podcast:edit")}')


#views test (logged in user)

class TestPodcastLoggedInViews(TestCase):

    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username="testuser")[0])
        self.test_podcast = models.Podcast.objects.create(
            title = "Podcast title",
            description = "Something about podcast",
            audio = SimpleUploadedFile('test_audio.mp3',b'file_content','audio/mpeg'),
            podcaster = get_user(self.client)
        )

    def test_logged_in_podcast_details_view(self):
        response = self.client.get(reverse("podcasts:details",kwargs={"pk":self.test_podcast.pk}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'podcasts/podcasts_details.html')

    def test_logged_in_podcast_details_POST_view(self):
        response = self.client.post(
            reverse("podcasts:details",kwargs={"pk":self.test_podcast.pk}),
            data={
                'content':"test comment",
            }
        )
        self.assertEqual(response.status_code,201)
        self.assertTemplateUsed(response,'podcasts/podcasts_details.html')

    def test_logged_in_add_podcast_view(self):
        response = self.client.get(reverse("podcasts:add"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'podcasts/add_podcasts.html')

    def test_logged_in_add_podcast_POST_view(self):
        response = self.client.post(
            reverse('podcasts:add'),
            data=
            {
            'title':'title of podcast',
            'description':'description of podcast',
            'banner':'title of podcast',
            'audio':SimpleUploadedFile('test_audio.mp3',b'file_content','audio/mpeg')
            }
        )
        self.assertEqual(response.status_code,201)
        self.assertTemplateUsed(response,'podcasts/add_podcasts.html')

    def test_logged_in_edit_podcast_view(self):
        response = self.client.get(reverse("podcasts:edit"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'podcasts/edit_podcasts.html')

    def test_logged_in_edit_podcast_POST_view(self):
        response = self.client.post(
            reverse('podcasts:edit'),
            data=
            {
            'title':'title of podcast',
            'description':'description of podcast',
            'banner':'title of podcast',
            'audio':SimpleUploadedFile('test_audio.mp3',b'file_content','audio/mpeg')
            }
        )
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'podcasts/edit_podcasts.html')
    