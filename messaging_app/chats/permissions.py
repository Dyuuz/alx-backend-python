# chats/permissions.py
from rest_framework import permissions
from .models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permission to ensure:
    1. Only authenticated and active users can access the API.
    2. Only participants of a conversation can send, view, update, or delete messages.
    """

    SAFE_METHODS = ["GET", "POST"]
    UNSAFE_METHODS = ["PUT", "PATCH", "DELETE"]

    def has_permission(self, request, view):
        # Must be authenticated + active
        if not (request.user.is_authenticated and request.user.is_active):
            return False

        # Allow GET and POST at general level
        if request.method in self.SAFE_METHODS:
            return True

        # For PUT, PATCH, DELETE → object permission will handle the check
        if request.method in self.UNSAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Object-level check for GET, POST, PUT, PATCH, DELETE.
        User must be a participant of the conversation.
        """

        # Check if object is a Conversation
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # Check if object is a Message with a conversation field
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False