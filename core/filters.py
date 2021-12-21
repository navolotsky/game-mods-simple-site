from django_filters import rest_framework as filters

from .models import Mod


class ModFilter(filters.FilterSet):
    class Meta:
        model = Mod
        fields = ["game__id", "category__id"]

    category__id = filters.NumberFilter(field_name="categories__id")
