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
                          MeUserSerializer, RequestCreateUserSerialise,
                          ReviewSerializer, TitleCreateSerializer,
                          TitleListSerializer, UsersSerializer)


class RequestCreateUserViewSet(viewsets.ViewSet):
    """Создает пользователя и отправляет код подтверждения на почту"""
    queryset = User.objects.all()
    serializer_class = RequestCreateUserSerialise
    http_method_names = ['post', ]

    def create(self, serializer):
        username = self.request.data.get('username')
        email = self.request.data.get('email')
        code = secrets.token_hex(16)

        if User.objects.filter(username=username, email=email).exists():
            user = User.objects.get(username=username)
            send_code_by_email(user)
            return Response(status=status.HTTP_200_OK)
        serializer = RequestCreateUserSerialise(data=self.request.data)
        if serializer.is_valid():
            serializer.save(confirmation_code=code, role='user')
            send_code_by_email(serializer.instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserViewSet(viewsets.ViewSet):
    """Проверяет код подтверждения и возвращает токен для
    авторизации пользователя"""
    queryset = User.objects.all()
    serializer_class = CreateUserSerialise
    http_method_names = ['post', ]

    def create(self, request):
        username = self.request.data.get('username')
        confirmation_code = self.request.data.get('confirmation_code')

        if not username or not confirmation_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        response = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)}
        return Response(data=response, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):
    """ВьюСет для работы с зарегистрированными пользователями"""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated, AdminPermissions)
    pagination_class = PageNumberPagination

    def list(self, request):
        queryset = User.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = UsersSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        serializer = UsersSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        serializer = UsersSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save(data=request.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if pk == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = get_object_or_404(User, username=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeUser(views.APIView):
    """ВьюСет для работы с персональной страницей по ссылке /users/me/ """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = MeUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        data = request.data.copy()
        user = get_object_or_404(User, username=request.user.username)
        if user.role == 'user':
            data['role'] = 'user'
        serializer = MeUserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
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

    def retrieve(self, request, pk=None):
        title = get_object_or_404(Title, pk=pk)
        serializer = TitleListSerializer(title)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
