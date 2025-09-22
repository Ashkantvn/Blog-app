from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ConfirmCode(models.Model):
    code= models.CharField(max_length=256, unique=True)
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} for {self.user.username}"
