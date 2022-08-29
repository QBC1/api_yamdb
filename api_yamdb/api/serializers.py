from rest_framework import exceptions, serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class ReviewSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=1, max_value=10)
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

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


class MeUserSerializer(serializers.ModelSerializer):
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
