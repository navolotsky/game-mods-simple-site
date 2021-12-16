from django.urls import include, path
from rest_framework import routers

from .views import GameViewSet, ModCategoryViewSet, ModViewSet, UserViewSet#,# GameMenuView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'games', GameViewSet)
# router.register(r'games-menu', GameViewSet.as_view({"get": "for_menu"}), basename="game2-menu")
router.register(r'categories', ModCategoryViewSet)
router.register(r'mods', ModViewSet)
# router.register(r'game_menu', GameMenuView)

urlpatterns = [path('', include(router.urls))]
