from django.urls import include, path
from rest_framework import routers

from api_yamdb.settings import VERSION_URL

from .views import (CategoryViewSet, CommentReviewViewSet, CreateUserViewSet,
                    GenreViewSet, MeUser, RequestCreateUserViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet)

router = routers.DefaultRouter()
router.register(r'auth/signup', RequestCreateUserViewSet, basename='signup')
router.register(r'auth/token', CreateUserViewSet, basename='token')
router.register(r'users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentReviewViewSet, basename='comments')

urlpatterns = [
    path(VERSION_URL + 'users/me/', MeUser.as_view()),
    path(VERSION_URL, include(router.urls)),
]
