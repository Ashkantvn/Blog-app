from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Contact(models.Model):
    subject = models.CharField(blank=True,null=False, max_length=50)
    content = models.TextField()
    email = models.EmailField(max_length=254)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="UNKNOWN",blank=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)