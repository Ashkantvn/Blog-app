from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify
from accounts.managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    profile_image = models.ImageField(
        upload_to='profiles/',
        default="profiles/default.png",
        blank=True
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    user_slug = models.SlugField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.user_slug:
            self.user_slug = slugify(self.username)
        super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']