from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.

class Podcast(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    banner = models.ImageField(default='fallback.png',blank=True)
    audio = models.FileField(upload_to='audio/')
    podcaster = models.ForeignKey(User,default=None,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
       self.slug = slugify(self.title)
       super(Podcast, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("podcasts:details", kwargs={"pk": self.pk})