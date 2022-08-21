from django.db import router
from django.urls import include, path
from rest_framework import routers

from .views import CreateUserViewSet, RequestCreateUserViewSet, UserViewSet

URL = 'api/v1/'

router = routers.DefaultRouter()
router.register(r'auth/signup', RequestCreateUserViewSet)
router.register(r'auth/token', CreateUserViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path(URL, include(router.urls)),
]
