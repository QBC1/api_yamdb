from django.urls import include, path
from rest_framework import routers

from .views import (
    CreateUserViewSet, RequestCreateUserViewSet,
    CategoryViewSet, GenreViewSet, TitleViewSet,
    ReviewViewSet, ReviewIDViewSet
)


router = routers.DefaultRouter()
router.register(r'auth/signup', RequestCreateUserViewSet)
router.register(r'auth/token', CreateUserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'^titles/(?P<title_id>\d+)/reviews/$', ReviewViewSet)
router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/$', ReviewIDViewSet)
# router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/$', )
# router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments(?P<comment_id>\d+)/$', )

urlpatterns = [
    path('v1/', include(router.urls)),
]
