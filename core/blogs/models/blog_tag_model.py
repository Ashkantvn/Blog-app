from django.db import models

class BlogTags(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    
    class Meta: indexes =[
        models.Index(fields=['blog']),
        models.Index(fields=['tag']),
        models.Index(fields=['blog', 'tag']), # optional combo 
    ]