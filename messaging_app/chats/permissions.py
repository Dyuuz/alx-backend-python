from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only participants of a conversation can GET or POST messages/conversations.
    """

    def has_permission(self, request, view):
        # Allow only authenticated and active users
        return request.user.is_authenticated and request.user.is_active

    def has_object_permission(self, request, view, obj):
        # Check if user is a participant
        if isinstance(obj, Conversation):
            is_participant = request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            is_participant = request.user in obj.conversation.participants.all()
        else:
            return False

        # Hardcode allowed methods: GET and POST
        if request.method in ["GET", "POST"]:
            return is_participant

        # Deny access for all other methods
        return False
