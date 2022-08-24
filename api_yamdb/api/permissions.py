from rest_framework import permissions


class PostRequestPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == 'POST'


# Categories, genres, titles
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее редактировать объект только
    администраторам.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.role == 'admin'
                         or request.user.is_superuser)))
