from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    slug = models.SlugField(max_length=60)
    banner = models.ImageField(default='fallback.png', blank=True)
    date_created = models.DateField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    author = models.ForeignKey(User, default=None , on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    tags = TaggableManager()
    status = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
       self.slug = slugify(self.title)
       super(Post, self).save(*args, **kwargs) # Call the real save() method


    def get_absolute_url(self):
        return reverse("posts:details", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['-date_created']
    

class Comment(models.Model):
    content = models.TextField()
    comment_for = models.ForeignKey(Post,default=None,on_delete=models.CASCADE)
    author = models.ForeignKey(User , default=None, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"comment by {self.author} on {self.created_date}"
    
    class Meta:
        ordering = ['-created_date']

class FavoritePost(models.Model):
    post = models.ForeignKey(Post,default=None,on_delete=models.CASCADE)
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorite post of {self.user}"