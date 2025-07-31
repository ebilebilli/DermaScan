from django.db import models

from users.models.user import CustomerUser
from scans.models.skin_image import SkinImage


class ChatMessage(models.Model):
    USER = 'user'
    AI = 'ai'
    sender_choose_list = [
        (USER, 'USER'),
        (AI, 'AI')
    ]

    user = models.ForeignKey(
        CustomerUser, 
        on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        SkinImage, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    sender = models.CharField(
        max_length=10,
        choices=sender_choose_list,
        editable=False,
        verbose_name='Sender'
        )  
    message = models.TextField(
        max_length=500,
        verbose_name='Message'
        )
   
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'Message from {self.user.id} at {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
    
    class Meta:
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'