from rest_framework.permissions import BasePermission

class OwnerShipPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_active and request.user.is_authenticated
    

    def has_object_permission(self, request, view, obj):
        
        return super().has_object_permission(request, view, obj)