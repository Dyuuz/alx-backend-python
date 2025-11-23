# chats/permissions.py
from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permission to ensure:
    1. Only authenticated and active users can access the API.
    2. Only participants of a conversation can send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        # Only authenticated and active users can access the API
        return request.user.is_authenticated and request.user.is_active

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        Only allow access if the user is a participant in the conversation
        or the message's conversation.
        """
        # If obj is a Conversation
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If obj is a Message (or has a conversation)
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        # Deny by default
        return False
