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
    terms_accepted = models.BooleanField(
        default=False,
        editable=False,
        verbose_name='Terms of Service'
        )
    is_active = models.BooleanField(
        default=True
    )
    is_premium = models.BooleanField(
        default=False
    )
    
    def __str__(self):
        return f'{self.username} - {self.email}'
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'