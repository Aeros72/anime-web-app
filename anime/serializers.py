from rest_framework import serializers
from .models import Anime, Genre, Favorite


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name',)


class AnimeSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Anime
        fields = (
            'id',
            'title',
            'description',
            'episodes',
            'score',
            'release_year',
            'status',
            'image',
            'genres',
        )


class FavoriteSerializer(serializers.ModelSerializer):
    anime_title = serializers.CharField(source="anime.title", read_only=True)
    anime_id = serializers.IntegerField(source="anime.id", read_only=True)

    anime = serializers.PrimaryKeyRelatedField(
        queryset=Anime.objects.all(),
        write_only=True
    )

    class Meta:
        model = Favorite
        fields = (
            "id",
            "anime",
            "anime_id",
            "anime_title",
            "created_at",
        )
