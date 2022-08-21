import secrets

from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User

from .permissions import PostRequestPermissions
from .serializers import (CreateUserSerialise, RequestCreateUserSerialise,
                          UsersSerializer)


def send_code_by_email(user):
    username = user.username
    code = user.confirmation_code
    email = user.email
    message = (
        f'''Для регистрации на сайте пройдите по ссылке:
            http://127.0.0.1:8000/api/v1/auth/token/
            с параметрами username: "{username}" confirmation_code="{code}"
            ''')
    send_mail(
        message=message,
        subject="Регистрация пользователя",
        recipient_list=[email, ],
        from_email="registration@yamdb.ru",)


class RequestCreateUserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = RequestCreateUserSerialise
    permission_classes = (PostRequestPermissions,)

    def create(self, serializer):
        username = self.request.data.get('username')
        email = self.request.data.get('email')
        code = secrets.token_hex(16)

        if User.objects.filter(username=username).filter(email=email).exists():
            user = User.objects.get(username=username)
            send_code_by_email(user)
            return Response(status=status.HTTP_200_OK)
        serializer = RequestCreateUserSerialise(data=self.request.data)
        if serializer.is_valid():
            serializer.save(confirmation_code=code, role='user')
            send_code_by_email(serializer.instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerialise
    permission_classes = (PostRequestPermissions,)

    def create(self, request):
        username = self.request.data.get('username')
        confirmation_code = self.request.data.get('confirmation_code')

        if not username or not confirmation_code or username == 'me':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(username=username).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not User.objects.filter(confirmation_code=confirmation_code).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(
            username=username).filter(confirmation_code=confirmation_code).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)
        refresh = RefreshToken.for_user(user)
        response = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)}
        return Response(data=response, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        if not request.user.role == 'admin':
            return Response(status=status.HTTP_403_FORBIDDEN)

        queryset = User.objects.all()
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if not request.user.role == 'admin':
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
