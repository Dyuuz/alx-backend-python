from rest_framework.permissions import BasePermission
from .models import Conversation

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow access only to users who are:
    - Active and authenticated
    - A participant of at least one conversation
    - Performing safe HTTP methods (GET, POST, etc.) if applicable
    """

    def has_permission(self, request, view):
        # Allow non-modifying methods without checking conversation participation
        safe_method = request.method not in ["PUT", "PATCH", "DELETE"]

        # Check if the user is active and authenticated
        if not (request.user.is_authenticated and request.user.is_active):
            return False

        # Check if the user is a participant in any conversation
        is_participant = Conversation.objects.filter(
            participants=request.user.user_id
        ).exists()

        # Final permission: safe method and participant
        return safe_method and is_participant
