from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    slug = models.SlugField(max_length=60)
    banner = models.ImageField(default='fallback.png', blank=True)
    date_created = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, default=None , on_delete=models.CASCADE)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
       self.slug = slugify(self.title)
       super(Post, self).save(*args, **kwargs) # Call the real save() method


    def get_absolute_url(self):
        return reverse("posts:details", kwargs={"pk": self.pk})
    

class Comment(models.Model):
    content = models.TextField()
    comment_for = models.ForeignKey(Post,default=None,on_delete=models.CASCADE)
    author = models.ForeignKey(User , default=None, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"comment by {self.author} on {self.created_date}"