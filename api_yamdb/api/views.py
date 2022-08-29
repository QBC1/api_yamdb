import secrets

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, permissions, status, views,
                            viewsets)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from .extra_functions import send_code_by_email
from .filters import TitleFilter
from .permissions import AdminPermissions, IsAdminOrReadOnly, ReadOrOwner
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateUserSerialise, GenreSerializer,
                          RequestCreateUserSerialise, ReviewSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          UsersSerializer)


class RequestCreateUserViewSet(viewsets.ViewSet):
    """Создает пользователя и отправляет код подтверждения на почту"""
    queryset = User.objects.all()
    serializer_class = RequestCreateUserSerialise
    http_method_names = ['post', ]

    def create(self, request):
        data = {
            'username': self.request.data.get('username'),
            'email': self.request.data.get('email'),
            'confirmation_code': secrets.token_hex(16)
        }
        serializer = RequestCreateUserSerialise(data=data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.create(**data)
            send_code_by_email(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUserViewSet(viewsets.ViewSet):
    """Проверяет код подтверждения и возвращает токен для
    авторизации пользователя"""
    queryset = User.objects.all()
    serializer_class = CreateUserSerialise
    http_method_names = ['post', ]

    def create(self, request):
        data = {
            'username': self.request.data.get('username'),
            'confirmation_code': self.request.data.get('confirmation_code')
        }
        serializer = CreateUserSerialise(data=data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User, username=data['username'])
            if user.confirmation_code != data['confirmation_code']:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        response = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)}
        return Response(data=response, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """ВьюСет для работы с зарегистрированными пользователями"""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated, AdminPermissions)
    pagination_class = PageNumberPagination

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        serializer = UsersSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        serializer = UsersSerializer(user, request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(data=request.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeUser(views.APIView):
    """ВьюСет для работы с персональной страницей по ссылке /users/me/ """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UsersSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        data = request.data.copy()
        if request.user.is_user:
            data['role'] = 'user'
        serializer = UsersSerializer(request.user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(data=data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами"""
    serializer_class = ReviewSerializer
    permission_classes = [ReadOrOwner, ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с коментариями к отзывам"""
    permission_classes = [ReadOrOwner, ]
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
