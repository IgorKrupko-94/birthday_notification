from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Follow
from .serializers import CustomUserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class FollowAPIView(APIView):
    def post(self, request, user_id):
        user_me = self.request.user
        follow_user = get_object_or_404(User, pk=user_id)
        if user_me.pk == user_id:
            raise ValidationError('Нельзя подписаться на самого себя!')
        Follow.objects.get_or_create(user=user_me, author=follow_user)
        return Response(status=status.HTTP_201_CREATED)


class UnfollowAPIView(APIView):
    def delete(self, request, user_id):
        user_me = self.request.user
        follow_user = get_object_or_404(User, pk=user_id)
        follow = get_object_or_404(Follow, user=user_me, author=follow_user)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
