import datetime as dt

from rest_framework import serializers

from reviews.models import UserForRegistarions, User, Category, Genre, Title


class RequestCreateUserSerialise(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email',)
        model = User


class CreateUserSerialise(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = UserForRegistarions


# Categories, genres, titles
class CategorySerializer(serializers.ModelSerializer):
    """Список категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Список жанров"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    """Запись произведения."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value


class TitleListSerializer(serializers.ModelSerializer):
    """Чтение произведений."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
