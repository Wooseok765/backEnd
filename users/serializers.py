from .models import User
from rest_framework.serializers import ModelSerializer


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "profile_photo",
            "username",
        ) # 방 정보 확인할 때 포함 할 유저정보


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        ) # 유저가 개인 프로필 변경간 못만지게 할 필드들
