from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.core.signals import request_finished
from .models import Message, Notification, MessageHistory
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Message)
def create_notification(sender, instance, **kwargs):
    receiver = instance.receiver
    Notification.objects.create(
        receiver=receiver,
        message=instance)
    logger.info(f"{instance} has been created")
    logger.info(f"Notification sent to: {instance.parent_message} at {instance.timestamp}")

@receiver(pre_save, sender=Message)
def create_message_history(sender, instance, **kwargs):
    try:
        old_content = Message.objects.get(id=instance.id)
    except Message.DoesNotExist:
        return 
    if instance.edited:
        mh=MessageHistory.objects.create(
            edited_by=instance.sender,
            old_content=old_content.content,
            recipient=instance.parent_message,
        )
        instance.edited=False
        logger.info(f"User: {instance.sender} => edited a message[{old_content.content}] to [{instance.content}] | Sent to {instance.parent_message} at {mh.edited_at}")

@receiver(post_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    print(instance.username, instance.date_joined)
    Message.objects.filter(sender=instance.username).delete()
    user_message_histories = MessageHistory.objects.filter(edited_by=instance.username)
    user_message_histories.delete()
    logger.info(f"Account deleted by user: {instance.username}")


@receiver(request_finished, sender=Message)
def read_messages(sender, instance, **kwargs):
    print(instance)
    instance.read=True
    print("Done")