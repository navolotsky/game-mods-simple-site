from django.urls import include, path
from rest_framework import routers

from .views import GameViewSet, ModCategoryViewSet, ModViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'games', GameViewSet)
router.register(r'categories', ModCategoryViewSet)
router.register(r'mods', ModViewSet)

urlpatterns = [path('', include(router.urls))]
