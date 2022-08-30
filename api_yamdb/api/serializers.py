from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers

from reviews.models import Category, Comment, Genre, Review, Title, User


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError('Вы не можете добавить более'
                                                  'одного отзыва на'
                                                  ' произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'


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
        if value.lower() == 'me':
            raise exceptions.ValidationError(
                "Нельзя создать пользователя с именем 'me'")
        if not value:
            raise exceptions.ValidationError(
                "Имя пользователя не должно быть пустым")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise exceptions.ValidationError(
                "Данный почтовый адрес уже зарегистрирован")
        return value


class CreateUserSerialise(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256)

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = User

    def validate_username(self, value):
        if value:
            return value
        raise exceptions.ValidationError()

    def validate_confirmation_code(self, value):
        if value:
            return value
        raise exceptions.ValidationError()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


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


class TitleListSerializer(serializers.ModelSerializer):
    """Чтение произведений."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
