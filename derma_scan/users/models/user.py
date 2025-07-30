from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.validators import validate_birthday


__all__ = [
    'CustomerUser',
]

class CustomerUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Email'  
        )
    username = models.CharField(
        unique=True,
        max_length=20,
        verbose_name='Username'
        )
    birthday = models.DateField(
        verbose_name='Birthday',
        validators=[validate_birthday],
        null=True,
        blank=True
        )
    bio = models.TextField(
        max_length=250,
        verbose_name='Bio',
        null=True,
        blank=True
        )
    profile_image = models.ImageField(
        upload_to='profile_images',
        verbose_name='Profile image',
        null=True,
        blank=True
        )
    
    def __str__(self):
        return f'{self.username} - {self.email}'
     