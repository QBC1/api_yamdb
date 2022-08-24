from django.db import router
from django.urls import include, path
from rest_framework import routers

from .views import (
    CreateUserViewSet, RequestCreateUserViewSet,
    CategoryViewSet, GenreViewSet, TitleViewSet,
)

URL = 'api/v1/'

router = routers.DefaultRouter()
router.register(r'auth/signup', RequestCreateUserViewSet)
router.register(r'auth/token', CreateUserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path(URL, include(router.urls)),
]
