from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read-only to anyone. Write allowed only to the owner (author).
    """

    def has_object_permission(self, request, view, obj):
        # Read-only allowed for anybody
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write allowed only if the requesting user is the author (owner)
        return hasattr(obj, 'author') and obj.author == request.user

