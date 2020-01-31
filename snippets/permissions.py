from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        # Check permissions for read-only request
        # SAFE_METHODS : which is a tuple containing 'GET', 'OPTIONS' and 'HEAD'.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        # Check permissions for write request
        return obj.owner == request.user
