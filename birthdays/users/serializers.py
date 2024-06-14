from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from .models import User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'birth_date', 'is_notification_agree')


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'birth_date', 'first_name',
                  'last_name', 'email')


class SendCongratulateSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
