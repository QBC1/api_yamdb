from rest_framework import permissions


class AdminPermissions(permissions.BasePermission):
    """Данный класс используем для работыс зарегистрированными
    пользователями"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_staff))


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение редактировать только администраторам."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin
                         or request.user.is_superuser)))


class ReadOrOwner(permissions.BasePermission):
    """Данный класс используем для работы с отзывами"""
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)
