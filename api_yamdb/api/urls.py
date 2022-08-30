from django.urls import include, path
from rest_framework import routers

from api_yamdb.settings import VERSION_URL

from .views import (CategoryViewSet, CommentReviewViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, confrim_user,
                    request_for_registration)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentReviewViewSet, basename='comments')

urlpatterns = [
    path(
        VERSION_URL + 'auth/signup/',
        request_for_registration, name='request_for_registration'),
    path(VERSION_URL + 'auth/token/', confrim_user, name='confrim_user'),
    path(VERSION_URL, include(router.urls))
]
