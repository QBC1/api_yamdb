from rest_framework import serializers

from reviews.models import UserForRegistarions, User


class RequestCreateUserSerialise(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email',)
        model = User


class CreateUserSerialise(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = UserForRegistarions
