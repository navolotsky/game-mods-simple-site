from django.db.models import F, FilteredRelation, Prefetch, Q
from rest_framework import viewsets
from rest_framework.decorators import action

from .filters import ModFilter
from .models import Game, Mod, ModCategory, ModVersion, User
from .pagination import StandardResultsSetPagination
from .serializers import GameMenuSerializer, GameSerializer, ModCategoryMenuSerializer, ModCategorySerializer, \
    ModDetailSerializer, \
    ModListSerializer, UserSerializer
from .services import get_games_queryset_for_menu, get_mod_categories_queryset_for_menu


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("profile").all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination


class ModViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (Mod.objects
                .select_related("game", "author", "default_version")
                .prefetch_related("categories")
                .filter(hidden=False,
                        default_version__isnull=False,
                        default_version__hidden=False))
    pagination_class = StandardResultsSetPagination
    filterset_class = ModFilter

    def get_queryset(self):
        if self.action == "list":
            return self.queryset.select_related("default_version__main_image")
        elif self.action == "retrieve":
            qs = self.queryset
            requested_version_id = self.request.query_params.get("version_id")
            # First check if a requested version exists on the mod
            qs = qs.annotate(requested_version=FilteredRelation("versions", condition=Q(
                versions__hidden=False,
                versions=requested_version_id if requested_version_id else F("default_version")))
                             ).filter(requested_version__isnull=False)
            # Then select the requested version
            qs = qs.prefetch_related(Prefetch("versions", queryset=ModVersion.objects.filter(
                hidden=False,
                id=requested_version_id if requested_version_id else F("mod__default_version")),
                                              to_attr="requested_version_one_element_list"))
            return qs.prefetch_related(Prefetch("versions", queryset=ModVersion.objects.filter(hidden=False)))
        else:
            raise RuntimeError(f"{self.action = } was unexpected")

    def get_serializer_class(self):
        if self.action == "list":
            return ModListSerializer
        elif self.action in ("retrieve", "create", "update", "partial_update"):
            return ModDetailSerializer
        else:
            raise RuntimeError(f"{self.action = } was unexpected")


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        if self.action == "get_list_for_menu":
            return get_games_queryset_for_menu(mods_category=self.request.query_params.get("mods_category_id"))
        return self.queryset

    def get_serializer_class(self):
        if self.action == "get_list_for_menu":
            return GameMenuSerializer
        return self.serializer_class

    @property
    def paginator(self):
        if self.action == "get_list_for_menu":
            return None
        else:
            return super().paginator

    @action(detail=False, methods=["get"])
    def get_list_for_menu(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ModCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModCategory.objects.all()
    serializer_class = ModCategorySerializer

    def get_queryset(self):
        if self.action == "get_list_for_menu":
            return get_mod_categories_queryset_for_menu(game=self.request.query_params.get("game_id"))
        return self.queryset

    def get_serializer_class(self):
        if self.action == "get_list_for_menu":
            return ModCategoryMenuSerializer
        return self.serializer_class

    @property
    def paginator(self):
        if self.action == "get_list_for_menu":
            return None
        else:
            return super().paginator

    @action(detail=False, methods=["get"])
    def get_list_for_menu(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
