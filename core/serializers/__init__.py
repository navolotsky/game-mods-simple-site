from rest_framework import serializers

from ._mod_detail_serializer import ModDetailSerializer
from ._mod_list_serializer import ModListSerializer
from ..models import Game, ModCategory, User, UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = UserProfile
            fields = ("avatar", "description")

    class Meta:
        model = User
        fields = ("id", 'username', "profile")

    profile = UserProfileSerializer()


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "name", "description"]


class ModCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModCategory
        fields = ["id", "name", "description"]
