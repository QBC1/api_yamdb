from django.urls import include, path
from rest_framework import routers

from api_yamdb.settings import VERSION_URL
from users.views import confrim_user, request_for_registration, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(
        VERSION_URL + 'auth/signup/',
        request_for_registration, name='request_for_registration'),
    path(VERSION_URL + 'auth/token/', confrim_user, name='confrim_user'),
    path(VERSION_URL, include(router.urls))
]
