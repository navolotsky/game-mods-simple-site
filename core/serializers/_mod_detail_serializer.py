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
        fields = ["title", "description", "main_image", "version_number", "images", "download_links",
                  "last_updated_at", "added_at"]

    description = serializers.CharField(source="full_description")
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
        fields = ["id", "game", "categories", "author", "content", "versions",
                  "default_version_id", "requested_version_id"]

    game = GameSerializer()
    categories = ModCategorySerializer(many=True)
    author = AuthorModSerializer()
    content = ModContentSerializer(source="requested_version")
    versions = ModVersionSerializer(many=True)
    default_version_id = serializers.IntegerField(source="default_version.id")
    requested_version_id = serializers.IntegerField(source="requested_version.id")

    def to_representation(self, instance):
        instance.requested_version = instance.requested_version_one_element_list[0]
        return super().to_representation(instance)
