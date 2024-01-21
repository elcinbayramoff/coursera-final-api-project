from rest_framework.permissions import BasePermission


class IsAdminOrManager(BasePermission):
    """
    Custom permission to allow only admin and manager group members.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.groups.filter(name='manager').exists())
class IsNotInAnyGroup(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user belongs to any groups
            return request.user.groups.count() == 0
        return False