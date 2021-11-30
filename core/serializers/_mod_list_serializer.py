from rest_framework import serializers

from ._mod_list_detail_shared_sub_serializers import *
from ..models import Mod, ModVersion

__all__ = ["ModListSerializer"]


class ModContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModVersion
        fields = ["title", "description", "main_image", "version_number", "last_updated_at", "added_at"]

    description = serializers.CharField(source="short_description")
    main_image = ModImageSerializer()
    version_number = serializers.CharField(source="number")


class ModListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mod
        fields = ["id", "game", "categories", "author", "content"]

    game = GameSerializer()
    categories = ModCategorySerializer(many=True)
    author = AuthorModSerializer()
    content = ModContentSerializer(source="showed_version")
