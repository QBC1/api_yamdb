import secrets

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import AdminPermissions
from users.models import User
from .extra_functions import send_code_by_email
from .serializers import (CreateUserSerialise, GetTokenSerialise,
                          UsersSerializer)


@api_view(['POSt', ])
def request_for_registration(request):
    serializer = CreateUserSerialise(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(confirmation_code=secrets.token_hex(16))
        send_code_by_email(serializer.instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def confrim_user(request):
    serializer = GetTokenSerialise(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = get_object_or_404(User, username=request.data.get('username'))
        if user.confirmation_code != request.data.get('confirmation_code'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    response = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)}
    return Response(data=response, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """ВьюСет для работы с зарегистрированными пользователями"""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated, AdminPermissions)

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs.get('pk'))
        return user

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UsersSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = UsersSerializer(
                request.user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                if request.user.is_user or request.user.is_moderator:
                    serializer.save(role=request.user.role)
                else:
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
