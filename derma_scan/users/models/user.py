from django.db import models
from django.contrib.auth.models import AbstractUser

from users.utils import validate_birthday


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
    is_active = models.BooleanField(
        default=True
    )
    is_premium = models.BooleanField(
        default=False
    )
    
    def __str__(self):
        return f'{self.username} - {self.email}'
     