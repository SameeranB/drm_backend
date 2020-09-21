from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    message = "You do not have the permissions to access this information"

    def has_object_permission(self, request, view, obj):
        return obj.is_owner(request.user) or request.user.is_staff


class IsOwner(permissions.BasePermission):
    message = "You do not have the permissions to access this information"

    def has_object_permission(self, request, view, obj):
        return obj.is_owner(request.user)


class IsOwnerOrAdminReadOnly(permissions.BasePermission):
    message = "You do not have the permissions to access this information"

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return obj.is_owner(request.user) or request.user.is_staff

        else:
            return obj.is_owner(request.user)
