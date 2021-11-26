from rest_framework import serializers

from ..models import Game, ModCategory, ModImage, User

__all__ = ["AuthorModSerializer", "GameSerializer", "ModCategorySerializer", "ModImageSerializer"]


class AuthorModSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "name"]


class ModCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModCategory
        fields = ["id", "name"]


class ModImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModImage
        fields = ["id", "url"]

    url = serializers.ImageField(source="file", read_only=True)
