from rest_framework import exceptions, serializers

from reviews.models import User


class RequestCreateUserSerialise(serializers.ModelSerializer):

    username = serializers.CharField(max_length=256)
    email = serializers.EmailField(max_length=256)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise exceptions.ValidationError(
                "Данное имя пользователя уже используется")
        if value == 'me':
            raise exceptions.ValidationError(
                "Нельзя создать пользователя с именем 'me'")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise exceptions.ValidationError(
                "Данный почтовый адрес уже зарегистрирован")
        return value


class CreateUserSerialise(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = User


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def validate_username(self, value):
        if len(value) < 7:
            raise exceptions.ValidationError(
                "Данное имя пользователя уже используется")
        return value
