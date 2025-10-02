from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)
    tag_slug = models.SlugField(unique=True, max_length=60)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag_name
    
    def save(self, *args, **kwargs):
        if not self.tag_slug or self.tag_slug != self.tag_name:
            self.tag_slug = slugify(self.tag_name)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['tag_name']