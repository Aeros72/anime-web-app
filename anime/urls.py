from rest_framework.routers import DefaultRouter
from .views import AnimeViewSet, FavoriteViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'anime', AnimeViewSet, basename='anime')
router.register(r'favorites', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls)),
]
