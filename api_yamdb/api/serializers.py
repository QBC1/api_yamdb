from rest_framework import serializers

from reviews.models import UserForRegistarions, User, Review


class RequestCreateUserSerialise(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email',)
        model = User


class CreateUserSerialise(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = UserForRegistarions


class ReviewSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
