from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outbox')
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, related_name='conversation', null=True, blank=True)   
    content = models.TextField(null=False, blank=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox')
    unread = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    objects = UnreadMessagesManager()

    def save(self, *args, **kwargs):
        if self.content:
            self.content = self.content.strip()
        super().save(*args, **kwargs)   

class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notification') 
    timestamp = models.DateTimeField(auto_now_add=True)

class MessageHistory(models.Model):
    edited_by = models.CharField(max_length=255, null=False, blank=True)
    old_content = models.TextField(null=False, blank=True)
    recipient = models.CharField(max_length=255, null=False, blank=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    




