from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Game, Mod, ModCategory, User
from .pagination import StandardResultsSetPagination
from .serializers import GameMenuSerializer, GameSerializer, ModCategorySerializer, ModDetailSerializer, \
    ModListSerializer, UserSerializer
from .services import get_games_queryset_for_menu


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("profile").all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination


class ModViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (Mod.objects
                .select_related("game", "author", "showed_version__main_image", "showed_version")
                .prefetch_related("categories")
                .filter(hidden=False,
                        showed_version__isnull=False,
                        showed_version__hidden=False))
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["game__id"]

    def get_serializer_class(self):
        if self.action == "list":
            return ModListSerializer
        elif self.action in ("retrieve", "create", "update", "partial_update"):
            return ModDetailSerializer
        else:
            raise ValueError(f"{self.action = } was unexpected")


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        if self.action == "get_list_for_menu":
            return get_games_queryset_for_menu()
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


class ModCategoryViewSet(viewsets.ModelViewSet):
    queryset = ModCategory.objects.all()
    serializer_class = ModCategorySerializer
