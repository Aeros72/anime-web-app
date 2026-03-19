from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Anime, Favorite
from .serializers import AnimeSerializer, FavoriteSerializer
from .pagination import AnimePagination
from .permissions import IsAdminOrReadOnly


class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all().prefetch_related("genres")
    serializer_class = AnimeSerializer
    pagination_class = AnimePagination
    permission_classes = [IsAdminOrReadOnly]


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
