from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    banner = models.ImageField(upload_to='blogs/',default='blogs/default.png')
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('Tag', related_name='blogs', through="BlogTags")
    is_published = models.BooleanField(default=False)
    publishable = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    published_date= models.DateField(null=True, blank=True)
    blog_slug = models.SlugField(unique=True, max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def get_absolute_url(self):
        return reverse("blogs:details", kwargs={"blog_slug": self.blog_slug})
    
    def get_edit_url(self):
        return reverse("blogs:edit", kwargs={"blog_slug": self.blog_slug})
    
    def get_delete_url(self):
        return reverse("blogs:delete", kwargs={"blog_slug": self.blog_slug})
    
    def save(self, *args, **kwargs):
        if not self.blog_slug or self.blog_slug != slugify(self.title):
            self.blog_slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published_date']
    