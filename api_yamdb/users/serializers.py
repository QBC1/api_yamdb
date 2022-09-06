from rest_framework import exceptions, serializers

from api_yamdb.settings import BLOCKED_NAMES
from users.models import User


class CreateUserSerialise(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value.lower() in BLOCKED_NAMES:
            raise exceptions.ValidationError(
                f"Нельзя создать пользователя с именем {value}")
        return value


class GetTokenSerialise(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256)

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
