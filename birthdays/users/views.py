from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Follow
from .serializers import CustomUserSerializer, SendCongratulateSerializer
from .tasks import send_congratulation_task


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с объектами модели User."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False)
    def get_following(self, request):
        """Получение подписок пользователя."""
        user_following = User.objects.prefetch_related(
            'follower', 'following').filter(following__user=request.user)
        serializer = self.get_serializer(user_following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def get_followers(self, request):
        """Получение подписчиков пользователя."""
        followers = User.objects.prefetch_related(
            'follower', 'following').filter(follower__author=request.user)
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def get_birthday_users(self, request):
        """Получение именинников."""
        current_date = timezone.now().date()
        users_with_birthday_today = User.objects.filter(
            birth_date__day=current_date.day,
            birth_date__month=current_date.month
        )
        serializer = self.get_serializer(users_with_birthday_today, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowAPIView(APIView):
    """APIView-класс для создания подписок."""
    def post(self, request, user_id):
        user_me = self.request.user
        follow_user = get_object_or_404(User, pk=user_id)
        if user_me.pk == user_id:
            raise ValidationError('Нельзя подписаться на самого себя!')
        Follow.objects.get_or_create(user=user_me, author=follow_user)
        return Response(status=status.HTTP_201_CREATED)


class UnfollowAPIView(APIView):
    """APIView-класс для удаления подписок."""
    def delete(self, request, user_id):
        user_me = self.request.user
        follow_user = get_object_or_404(User, pk=user_id)
        follow = get_object_or_404(Follow, user=user_me, author=follow_user)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CongratulateAPIView(APIView):
    """APIView-класс для отправки сообщений с поздравлениями."""
    def post(self, request, user_id):
        serializer = SendCongratulateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_birthday = get_object_or_404(User, pk=user_id)
        send_congratulation_task.delay(user_birthday.email,
                                       serializer.validated_data['message'])
        return Response(status=status.HTTP_200_OK)
