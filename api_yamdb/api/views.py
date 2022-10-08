import secrets

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title, User
from .extra_functions import send_code_by_email
from .filters import TitleFilter
from .mixins import ModelMixins
from .permissions import AdminPermissions, IsAdminOrReadOnly, ReadOrOwner
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateUserSerialise, GenreSerializer,
                          RequestCreateUserSerialise, ReviewSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          UsersSerializer)


@api_view(['POSt', ])
def request_for_registration(request):
    serializer = RequestCreateUserSerialise(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(confirmation_code=secrets.token_hex(16))
    send_code_by_email(serializer.instance)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def confrim_user(request):
    serializer = CreateUserSerialise(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=serializer.validated_data['username'])
    if user.confirmation_code != serializer.validated_data[
        'confirmation_code'
    ]:
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

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs.get('pk'))
        return user

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):

        if request.method == 'GET':
            serializer = UsersSerializer(request.user)

            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = UsersSerializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if request.user.is_user or request.user.is_moderator:
                serializer.save(role=request.user.role)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Categories, genres, titles
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
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all().order_by('name')
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
