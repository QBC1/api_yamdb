from django.urls import include, path
from rest_framework import routers

from .views import (CreateUserViewSet, MeUser, RequestCreateUserViewSet,
                    UserViewSet)
from .views import (
    CreateUserViewSet, MeUser, RequestCreateUserViewSet, UserViewSet,
    CategoryViewSet, GenreViewSet, TitleViewSet,
    ReviewViewSet, ReviewIDViewSet
)


router = routers.DefaultRouter()
router.register(r'auth/signup', RequestCreateUserViewSet)
router.register(r'auth/token', CreateUserViewSet)
router.register(r'users', UserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'^titles/(?P<title_id>\d+)/reviews/$', ReviewViewSet)
router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/$', ReviewIDViewSet)
# router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/$', )
# router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments(?P<comment_id>\d+)/$', )

urlpatterns = [
    path(URL + 'users/me/', MeUser.as_view()),
    path(URL, include(router.urls)),
]
