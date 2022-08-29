from rest_framework import serializers
from django.utils import timezone as tz


def validate_year(value):
    current_year = tz.now().year
    if value > current_year:
        raise serializers.ValidationError(
            'Год выпуска не может быть больше текущего'
        )
    return value
