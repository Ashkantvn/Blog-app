from django.test import SimpleTestCase , TestCase, Client
from django.urls import reverse,resolve
from .views import users_login_view,users_logout_view,users_register_view

# Create your tests here.

# test Urls
class UsersTestUrls(SimpleTestCase):

    def test_user_login_url_is_resolve(self):
        url = reverse("users:login")
        self.assertEqual(resolve(url).func,users_login_view)


    def test_user_register_url_is_resolve(self):
        url = reverse("users:register")
        self.assertEqual(resolve(url).func,users_register_view)


    def test_user_logout_url_is_resolve(self):
        url = reverse("users:logout")
        self.assertEqual(resolve(url).func,users_logout_view)



# test views
class UsersTestViews(TestCase):
    
    def setup(self):
        self.client = Client()


    def test_login_GET(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"users/users_login.html")

    
    def test_register_GET(self):
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"users/users_register.html")