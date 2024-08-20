from django.test import SimpleTestCase , TestCase, Client
from django.urls import reverse,resolve
from .views import users_login_view,users_logout_view,users_register_view,users_view,users_change_pass_view
from django.contrib.auth.models import User
from django.contrib import auth
from posts import models as post_models

# Create your tests here.

# test Urls
class UsersTestUrls(SimpleTestCase):
    def test_user_info_url_is_resolve(self):
        url=reverse("users:info")
        self.assertEqual(resolve(url).func,users_view)

    def test_user_login_url_is_resolve(self):
        url = reverse("users:login")
        self.assertEqual(resolve(url).func,users_login_view)


    def test_user_register_url_is_resolve(self):
        url = reverse("users:register")
        self.assertEqual(resolve(url).func,users_register_view)


    def test_user_logout_url_is_resolve(self):
        url = reverse("users:logout")
        self.assertEqual(resolve(url).func,users_logout_view)

    def test_user_chagnge_password_is_resolve(self):
        url = reverse("users:change-pass")
        self.assertEqual(resolve(url).func,users_change_pass_view)



# test views
class UsersTestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        self.test_post = post_models.Post.objects.create(
            title = "test post",
            content = 'testcontent',
            author = auth.get_user(self.client)
        )
        self.test_comment = post_models.Comment.objects.create(
            content = "test comment",
            comment_for = self.test_post,
            author = auth.get_user(self.client)
        )

    def test_login_GET(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"users/users_login.html")

    def test_authentication(self):
        response = self.client.get(reverse("users:info"))
        self.assertEqual(response.status_code,200)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
    
    def test_info_POST(self):
        response = self.client.post(
            reverse("users:info"),
            data={
                "_method" : "DELETE",
                "comment": self.test_comment.pk,
            }    
        )
        self.assertNotIn(self.test_comment,post_models.Comment.objects.all())
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('users:info'))

    
    def test_register_GET(self):
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"users/users_register.html")

    def test_logout_GET(self):
        response = self.client.get(reverse("users:logout"))
        self.assertRedirects(response, reverse("users:login"))
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_user_change_pass_GET(self):
        response = self.client.get(reverse("users:change-pass"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"users/users_change_pass.html")