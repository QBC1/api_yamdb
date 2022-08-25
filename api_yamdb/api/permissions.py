from rest_framework import exceptions, permissions


class AdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'role'):
            if request.user.role == 'admin' or request.user.is_staff:
                return True
            else:
                raise exceptions.PermissionDenied()
        raise exceptions.NotAuthenticated()
