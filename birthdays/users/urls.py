from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, FollowAPIView, UnfollowAPIView,
                    CongratulateAPIView)

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('follow/<int:user_id>', FollowAPIView.as_view()),
    path('unfollow/<int:user_id>', UnfollowAPIView.as_view()),
    path('congratulate/<int:user_id>', CongratulateAPIView())
]
