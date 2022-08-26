from rest_framework import exceptions, permissions


class AdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'role'):
            if request.user.role == 'admin' or request.user.is_staff:
                return True
            else:
                raise exceptions.PermissionDenied()
        raise exceptions.NotAuthenticated()


# Categories, genres, titles
class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение редактировать только администраторам."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.role == 'admin'
                         or request.user.is_superuser)))


class ReviewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == 'POST'


class ReadOnlyOrAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
