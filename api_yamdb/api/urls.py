from django.db import router
from django.urls import include, path
from rest_framework import routers

from .views import CreateUserViewSet, RequestCreateUserViewSet

URL = 'api/v1/'

router = routers.DefaultRouter()
router.register(r'auth/signup', RequestCreateUserViewSet)
router.register(r'auth/token', CreateUserViewSet)

urlpatterns = [
    path(URL, include(router.urls)),
]
