from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permission to ensure that only participants of a conversation
    can send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        """
        General permission: allow only authenticated and active users.
        """
        return request.user.is_authenticated and request.user.is_active

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission: allow access only if the user
        is a participant in the conversation.
        """
        # For Conversation objects
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # For Message objects (assuming Message model has a conversation field)
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        # Deny access by default
        return False
