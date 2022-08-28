from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentReviewViewSet, CreateUserViewSet,
                    GenreViewSet, MeUser, RequestCreateUserViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet)

URL = 'v1/'

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
    path(URL + 'users/me/', MeUser.as_view()),
    path(URL, include(router.urls)),
]
