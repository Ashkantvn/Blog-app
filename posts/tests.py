from django.test import TestCase , SimpleTestCase,Client
from django.urls import reverse,resolve
from . import views,models
from django.contrib.auth.models import User
from django.contrib import auth

# Create your tests here.
class PostsUrlTests(SimpleTestCase):

    def test_post_list_url_is_resolve(self):
        url = reverse("posts:list")
        self.assertEqual(resolve(url).func,views.posts_list_view)

    def test_post_detail_url_is_resolve(self):
        url = reverse("posts:details",kwargs={"pk":1})
        self.assertEqual(resolve(url).func,views.posts_details_view)

    def test_add_post_url_is_resolve(self):
        url = reverse("posts:add")
        self.assertEqual(resolve(url).func,views.posts_add_view)

    def test_edit_post_url_is_resolve(self):
        url = reverse("posts:edit")
        self.assertEqual(resolve(url).func,views.posts_edit_view)

    def test_delete_url_is_resolve(self):
        url = reverse("posts:delete")
        self.assertEqual(resolve(url).func,views.posts_delete_view)




class PostsModelsTest(TestCase):
    def setUp(self):
        self.client  = Client()
        self.client.force_login(User.objects.get_or_create(username="testuser")[0])
        self.testPost = models.Post.objects.create(
            title = "test post",
            content = 'testcontent',
            author = auth.get_user(self.client)
        )

    def test_create_slug(self):
        self.assertEqual(self.testPost.slug , "test-post")

    def test_created_object_is_correct(self):
        self.assertEqual(self.testPost.title , "test post")