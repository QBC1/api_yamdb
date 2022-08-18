from django.db import router
from django.urls import include, path
from rest_framework import routers

from .views import RequestCreateUserViewSet

URL = 'api/v1/'

router = routers.DefaultRouter()
router.register(r'auth/signup', RequestCreateUserViewSet)


urlpatterns = [
    path(URL, include(router.urls)),
]
