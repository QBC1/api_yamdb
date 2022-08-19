import datetime
import secrets

from django.core.mail import send_mail
from rest_framework import exceptions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User, UserForRegistarions

from .permissions import PostRequestPermissions
from .serializers import CreateUserSerialise, RequestCreateUserSerialise


class RequestCreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RequestCreateUserSerialise
    permission_classes = (PostRequestPermissions,)

    def perform_create(self, request):
        username = self.request.data.get('username')
        email = self.request.data.get('email')
        code = secrets.token_hex(16)

        if (
            UserForRegistarions.objects.filter(username=username).exists()
            or UserForRegistarions.objects.filter(email=email).exists()):
            raise exceptions.ValidationError("Запрос с такими данными уже был отправлен")

        UserForRegistarions.objects.create(
            username=username, email=email, confirmation_code=code)
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


class CreateUserViewSet(viewsets.ViewSet):
    queryset = UserForRegistarions.objects.all()
    serializer_class = CreateUserSerialise
    permission_classes = (PostRequestPermissions,)

    def create(self, request):
        username = self.request.data.get('username')
        confirmation_code = self.request.data.get('confirmation_code')
        life_time_for_request = datetime.datetime.now() - datetime.timedelta(minutes=10)
        users_for_delete = UserForRegistarions.objects.filter(
            create_date__lt=life_time_for_request)
        users_for_delete.delete()

        if not UserForRegistarions.objects.filter(
            username=username).filter(
                confirmation_code=confirmation_code).exists():
            raise exceptions.ValidationError(
                "Не корректные данные пользователя")

        user_data = UserForRegistarions.objects.filter(
            username=username).filter(confirmation_code=confirmation_code)[0]

        if user_data and confirmation_code == user_data.confirmation_code:
            try:
                user = User.objects.create(
                    username=username,
                    email=user_data.email,
                    role="user")
            except Exception as e:
                raise exceptions.ValidationError(
                    f"Пользователь с данным именем или email уже существует ({e})")

            user_data.delete()
            refresh = RefreshToken.for_user(user)
            response = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)}
            return Response(data=response, status=status.HTTP_200_OK)

