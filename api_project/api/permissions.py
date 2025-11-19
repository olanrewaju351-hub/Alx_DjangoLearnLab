# api/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadCreateUpdateOnly(BasePermission):
    """
    Allow safe methods for everyone.
    Allow POST/PUT/PATCH only for authenticated users.
    Allow DELETE only for staff (is_staff).
    """
    def has_permission(self, request, view):
        # allow safe methods for anyone
        if request.method in SAFE_METHODS:
            return True

        # DELETE only for staff
        if request.method == 'DELETE':
            return bool(request.user and request.user.is_staff)

        # other unsafe methods (POST, PUT, PATCH) require authentication
        return bool(request.user and request.user.is_authenticated)

