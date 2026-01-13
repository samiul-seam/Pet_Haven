from rest_framework import permissions

class IsAdminOrReadAndPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == 'POST' and request.user and request.user.is_authenticated:
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        
        return obj.user == request.user
