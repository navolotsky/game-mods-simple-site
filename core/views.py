from rest_framework import viewsets

from .models import Game, Mod, ModCategory, User
from .pagination import StandardResultsSetPagination
from .serializers import GameSerializer, ModCategorySerializer, ModDetailSerializer, ModListSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("profile").all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination


class ModViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Mod.objects.filter(hidden=False, showed_version__isnull=False, showed_version__hidden=False)
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == "list":
            return ModListSerializer
        elif self.action in ("retrieve", "create", "update", "partial_update"):
            return ModDetailSerializer
        else:
            raise ValueError(f"{self.action = } was unexpected")


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class ModCategoryViewSet(viewsets.ModelViewSet):
    queryset = ModCategory.objects.all()
    serializer_class = ModCategorySerializer
