from rest_framework.permissions import BasePermission
from .models import Conversation

class IsParticipantOfConversation(BasePermission):


    def has_permission(self, request, view):
        print(request.method)
        active = request.user.is_active
        authenticated = request.user.is_authenticated
        method = request.method not in ["PUT", "PATCH", "DELETE"]
        user_belong = Conversation.objects.filter(participants=request.user.user_id).exists()
        return active and authenticated and method and user_belong

    # def has_object_permission(self, request, view, obj):
    #     if request.method not in ["PUT", "PATCH", "DELETE", "GET", "POST"]:
    #         return request.user in obj.participants.all()
    #     return False
        
