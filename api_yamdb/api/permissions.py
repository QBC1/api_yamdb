from rest_framework import permissions


class PostRequestPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == 'POST'


class UsersPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
 
    # Определяет права на уровне объекта
    def has_object_permission(self, request, view, obj):
        return True 