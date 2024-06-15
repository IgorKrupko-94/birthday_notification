from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from .models import User


class CustomUserSerializer(UserSerializer):
    """Кастомный сериализатор для десериализации объектов модели User."""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'birth_date', 'is_notification_agree')


class CustomUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для создания объектов модели User."""
    class Meta:
        model = User
        fields = ('username', 'password', 'birth_date', 'first_name',
                  'last_name', 'email')


class SendCongratulateSerializer(serializers.Serializer):
    """Сериализатор для обработки сообщений, отправляемых пользователям."""
    message = serializers.CharField(max_length=1000)
