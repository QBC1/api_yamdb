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
router.register(r'auth/signup', RequestCreateUserViewSet, basename='signup')
router.register(r'auth/token', CreateUserViewSet, basename='token')
router.register(r'users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'^titles/(?P<title_id>\d+)/reviews/$', ReviewViewSet, basename='reviews-list')
router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/$', ReviewIDViewSet, basename='reviews-detail')
# router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/$', )
# router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments(?P<comment_id>\d+)/$', )

urlpatterns = [
    path('v1/' + 'users/me/', MeUser.as_view()),
    path('v1/', include(router.urls)),
]
