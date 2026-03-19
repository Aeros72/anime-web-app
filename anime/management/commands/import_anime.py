import requests
import time
from django.core.management.base import BaseCommand
from anime.models import Anime, Genre


class Command(BaseCommand):
    help = "Import anime from Jikan API with pagination and error handling"

    def handle(self, *args, **kwargs):
        total_pages = 5
        for page in range(1, total_pages + 1):
            self.stdout.write(f"Importing page {page}...")

            url = f"https://api.jikan.moe/v4/anime?page={page}"

            for attempt in range(3):
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    break
                except requests.exceptions.RequestException as e:
                    self.stdout.write(self.style.WARNING(f"Attempt {attempt+1} failed for page {page}: {e}"))
                    time.sleep(2)
            else:
                self.stdout.write(self.style.ERROR(f"Failed to fetch page {page}"))
                continue


            if "data" not in data:
                self.stdout.write(self.style.WARNING(f"Page {page} has no 'data'"))
                time.sleep(2)
                continue

            for item in data["data"]:
                anime, created = Anime.objects.update_or_create(
                    title=item["title"],
                    defaults={
                        "description": item.get("synopsis") or "",
                        "episodes": item.get("episodes"),
                        "score": item.get("score"),
                        "release_year": item.get("year"),
                        "status": self.map_status(item.get("status")),
                        "image": item.get("images", {}).get("jpg", {}).get("image_url", ""),
                    }
                )

                for genre_data in item.get("genres", []):
                    genre, _ = Genre.objects.get_or_create(name=genre_data["name"])
                    anime.genres.add(genre)

            time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Import completed"))

    def map_status(self, status):
        mapping = {
            "Finished Airing": "finished",
            "Currently Airing": "ongoing",
            "Not yet aired": "upcoming",
        }
        return mapping.get(status, "finished")