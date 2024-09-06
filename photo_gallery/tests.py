from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from . import views

# Create your tests here.

# Url tests
class PhotoGalleryUrlTest(SimpleTestCase):

    def test_photo_gallery_list_is_resolved(self):
        url = reverse('photoGallery:list')
        self.assertEqual(resolve(url).func,views.gallery_view)