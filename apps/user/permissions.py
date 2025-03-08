from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view): # type: ignore
        return bool(request.user and request.user.is_superuser)
    
    def has_object_permission(self, request, view, obj): # type: ignore
        return False if obj.is_superuser and obj != request.user else True

class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view): # type: ignore
        return bool(request.user and request.user.is_staff and not request.user.is_superuser)
    
    def has_object_permission(self, request, view, obj): # type: ignore
        return False if obj.is_superuser or obj.is_staff and obj != request.user else True

class IsRegularUser(permissions.BasePermission):
    def has_permission(self, request, view): # type: ignore
        return bool(request.user and not request.user.is_staff)
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user