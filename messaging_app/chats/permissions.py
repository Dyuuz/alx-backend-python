from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to ensure that users can only access
    conversations and messages they are a participant of.
    """

    def has_permission(self, request, view):
        """
        General permission: allow authenticated and active users.
        """
        return request.user.is_authenticated and request.user.is_active

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission: only allow access if the user is
        a participant in the conversation or the owner of the message.
        """
        # For Conversation objects
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # For Message objects (assuming Message model has conversation and sender fields)
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False
