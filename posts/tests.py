from django.test import TestCase , SimpleTestCase
from django.urls import reverse,resolve
from . import views

# Create your tests here.
class PostsUrlTests(SimpleTestCase):

    def test_post_list_url_is_resolve(self):
        url = reverse("posts:list")
        self.assertEqual(resolve(url).func,views.posts_list_view)

    def test_post_detail_url_is_resolve(self):
        url = reverse("posts:details")
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
    