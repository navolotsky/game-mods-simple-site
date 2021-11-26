from rest_framework import serializers

from ._mod_list_detail_shared_sub_serializers import *
from ..models import Mod, ModDownloadLink, ModVersion

__all__ = ["ModDetailSerializer"]


class ModDownloadLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModDownloadLink
        fields = ["id", "url", "comment", "last_updated_at"]


class ModContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModVersion
        fields = ["title", "full_description", "main_image", "version_number", "images", "download_links",
                  "last_updated_at", "added_at"]

    main_image = ModImageSerializer()
    version_number = serializers.CharField(source="number")
    images = ModImageSerializer(many=True)
    download_links = ModDownloadLinkSerializer(many=True)


class ModVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModVersion
        fields = ["id", "version_number", "comment", "last_updated_at", "added_at"]

    version_number = serializers.CharField(source="number")


class ModDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mod
        fields = ["id", "game", "categories", "author", "content", "versions"]

    game = GameSerializer()
    categories = ModCategorySerializer(many=True)
    author = AuthorModSerializer()
    content = ModContentSerializer(source="showed_version")
    versions = ModVersionSerializer(many=True)
