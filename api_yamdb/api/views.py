import datetime
import secrets

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import exceptions, status, viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import (
    User, UserForRegistarions,
    Category, Genre, Title,
    Review
)
from .permissions import (
    PostRequestPermissions, IsAdminOrReadOnly,
    ReviewPermission, ReadOnlyOrAuthor
    
)
from .serializers import (
    CreateUserSerialise, RequestCreateUserSerialise,
    CategorySerializer, GenreSerializer,
    TitleCreateSerializer, TitleListSerializer,
    ReviewSerializer
)
from .filters import TitleFilter


class RequestCreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RequestCreateUserSerialise
    permission_classes = (PostRequestPermissions,)

    def perform_create(self, request):
        username = self.request.data.get('username')
        email = self.request.data.get('email')
        code = secrets.token_hex(16)

        if (
            UserForRegistarions.objects.filter(username=username).exists()
            or UserForRegistarions.objects.filter(email=email).exists()):
            raise exceptions.ValidationError("Запрос с такими данными уже был отправлен")

        UserForRegistarions.objects.create(
            username=username, email=email, confirmation_code=code)
        message = (
            f'''Для регистрации на сайте пройдите по ссылке:
            http://127.0.0.1:8000/api/v1/auth/token/
            с параметрами username: "{username}" confirmation_code="{code}"
            ''')

        send_mail(
            message=message,
            subject="Регистрация пользователя",
            recipient_list=[email, ],
            from_email="registration@yamdb.ru",)


class CreateUserViewSet(viewsets.ViewSet):
    queryset = UserForRegistarions.objects.all()
    serializer_class = CreateUserSerialise
    permission_classes = (PostRequestPermissions,)

    def create(self, request):
        username = self.request.data.get('username')
        confirmation_code = self.request.data.get('confirmation_code')
        life_time_for_request = datetime.datetime.now() - datetime.timedelta(minutes=10)
        users_for_delete = UserForRegistarions.objects.filter(
            create_date__lt=life_time_for_request)
        users_for_delete.delete()

        if not UserForRegistarions.objects.filter(
            username=username).filter(
                confirmation_code=confirmation_code).exists():
            raise exceptions.ValidationError(
                "Не корректные данные пользователя")

        user_data = UserForRegistarions.objects.filter(
            username=username).filter(confirmation_code=confirmation_code)[0]

        if user_data and confirmation_code == user_data.confirmation_code:
            try:
                user = User.objects.create(
                    username=username,
                    email=user_data.email,
                    role="user")
            except Exception as e:
                raise exceptions.ValidationError(
                    f"Пользователь с данным именем или email уже существует ({e})")

            user_data.delete()
            refresh = RefreshToken.for_user(user)
            response = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)}
            return Response(data=response, status=status.HTTP_200_OK)


# Categories, genres, titles
class ModelMixins(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для наследования"""
    pass


class CategoryViewSet(ModelMixins):
    """Получаем список категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'


class GenreViewSet(ModelMixins):
    """Получаем список жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Получаем список произведений"""
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        """Возвращает подходящий сериализатор"""
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleCreateSerializer


class ReviewViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ReviewPermission
    pagination_class = LimitOffsetPagination
    # def get_queryset(self):
    #     title_id = self.kwargs.get('title_id')
    #     title = get_object_or_404(Title, id=title_id)
    #     return title.RELATED_NAME.all()


class ReviewIDViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin,
               mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ReadOnlyOrAuthor

    # def get_queryset(self):
    #     title_id = self.kwargs.get('title_id')
    #     title = get_object_or_404(Title, id=title_id)
    #     review_id = self.kwargs.get('review_id')
    #     review = get_object_or_404(Review, id=review_id)
    #     return title.RELATED_NAME.filter(review=review)
