"""
Custom permissions for RBAC
"""
from rest_framework import permissions


class HasPermission(permissions.BasePermission):
    """
    Custom permission to check if user has specific permission
    """
    def __init__(self, resource, action):
        self.resource = resource
        self.action = action
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.has_permission(self.resource, self.action)


def permission_required(resource, action):
    """
    Decorator to check permissions on view functions
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.has_permission(resource, action):
                from rest_framework.response import Response
                from rest_framework import status
                return Response(
                    {
                        'success': False,
                        'error': {
                            'code': 'PERMISSION_DENIED',
                            'message': 'You do not have permission to perform this action'
                        }
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners to edit
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.user == request.user or request.user.is_staff


class IsStaffUser(permissions.BasePermission):
    """
    Permission to check if user is staff
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff