import secrets

from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import UserForRegistarions
from .serializers import RequestCreateUserSerialise


class RequestCreateUserViewSet(viewsets.ModelViewSet):
    queryset = UserForRegistarions.objects.all()
    serializer_class = RequestCreateUserSerialise

    def perform_create(self, serializer):
        username = self.request.data.get('username')
        email = self.request.data.get('email')
        code = secrets.token_hex(16)
        serializer.save(confirm_code=code)
        message = (
            f'''Для регистрации на сайте пройдите по ссылке:
            http://127.0.0.1/api/v1/auth/token/?username={username}&code={code}
            ''')
        send_mail(
            message=message,
            subject="Регистрация пользователя",
            recipient_list=[email, ],
            from_email="registration@yamdb.ru",)
