from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Anime(models.Model):
    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("finished", "Finished"),
        ("upcoming", "Upcoming"),
    ]

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    episodes = models.IntegerField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    image = models.URLField(blank=True)

    genres = models.ManyToManyField(Genre, related_name="anime")

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "anime")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.email} -> {self.anime.title}"
