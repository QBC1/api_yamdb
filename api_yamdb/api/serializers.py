from rest_framework import serializers

from reviews.models import UserForRegistarions


class RequestCreateUserSerialise(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email',)
        model = UserForRegistarions

