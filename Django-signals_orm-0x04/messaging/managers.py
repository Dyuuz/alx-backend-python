from django.db import models

class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(unread=True)