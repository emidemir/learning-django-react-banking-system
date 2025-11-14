from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOfAccount(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            # Read permissions - user can view if they own either account
            return (obj.send_from and obj.send_from.user == request.user) or (obj.send_to and obj.send_to.user == request.user)
        else:
            # Write permissions - user must own the send_from account
            return obj.send_from and obj.send_from.user == request.user