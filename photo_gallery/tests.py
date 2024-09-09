from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from . import views

# Create your tests here.

# Url tests
class PhotoGalleryUrlTest(SimpleTestCase):

    def test_photo_gallery_list_is_resolved(self):
        url = reverse('photoGallery:list')
        self.assertEqual(resolve(url).func,views.gallery_view)

    def test_photo_gallery_posts_is_resolve(self):
        url = reverse('photoGallery:posts')
        self.assertEqual(resolve(url).func,views.post_gallery)


#views tests
class PhotoGalleryViewsTest(TestCase):

    def test_photo_gallery_list_views(self):
        response = self.client.get(reverse('photoGallery:list'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'photo_gallery/list.html')