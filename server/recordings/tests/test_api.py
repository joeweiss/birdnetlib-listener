from django.test import TestCase
from unittest import skipIf
from django.contrib.auth import get_user_model
from random import choice
from rest_framework.test import APIClient
import random
from recordings import models as app_models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from pprint import pprint
from django.conf import settings

User = get_user_model()


# watchmedo shell-command -c "python manage.py test recordings.tests.test_api --failfast --keepdb" --recursive -W


class ApiTestCase(TestCase):
    def test_user_list(self):
        User.objects.create(email="test@example.com")
        client = APIClient()
        response = client.get("/api/users/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"email": "test@example.com"}])

    def test_hearing_now_list(self):
        recording = app_models.Recording.objects.create()

        species_objs = []
        for i in range(0, 10):
            species = app_models.Species.objects.create(
                common_name=f"Bird {i}", scientific_name=f"Science {i}"
            )
            species_objs.append(species)

        analyzer = app_models.Analyzer.objects.create(name="Analyzer model 1.0")

        analysis = app_models.Analysis.objects.create(
            recording=recording, analyzer=analyzer
        )

        # Recent detections
        for i in range(0, 5):
            app_models.Detection.objects.create(
                recording=recording,
                species=choice(species_objs),
                analyzer=analyzer,
                analysis=analysis,
                confidence=random.uniform(0.5, 1.0),
                detected_at=timezone.now(),
            )

        # Detections 90 minutes ago.
        ninety_minutes_ago = timezone.now() - timedelta(minutes=90)
        for i in range(0, 100):
            app_models.Detection.objects.create(
                recording=recording,
                species=choice(species_objs),
                analyzer=analyzer,
                analysis=analysis,
                confidence=random.uniform(0.5, 1.0),
                detected_at=ninety_minutes_ago,
            )

        client = APIClient()
        response = client.get("/api/now-detections/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 5)

        client = APIClient()
        response = client.get("/api/now-detections/?minutes=100")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 105)

        response = client.get("/api/today-detections/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 105)

        # Get today's species query.
        species_today = (
            app_models.Detection.objects.all()
            .filter(detected_at__date=timezone.now())
            .values("species__common_name", "species__scientific_name")
            .annotate(count=Count("species"))
            .order_by("-count")
            .distinct()
        )
        # print(species_today)

        response = client.get("/api/daily-species/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # pprint(data)
        self.assertEqual(len(data), len(species_today))

        # Get the detected species for yesterday.
        yesterday = timezone.now() - timedelta(days=1)
        response = client.get(
            f"/api/daily-species/?start_date={yesterday.strftime('%Y-%m-%d')}&end_date={yesterday.strftime('%Y-%m-%d')}"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        pprint(data)
        self.assertEqual(len(data), 0)

        # Get the detected species for a range.
        yesterday = timezone.now() - timedelta(days=1)
        print(
            f"/api/daily-species/?start_date={yesterday.strftime('%Y-%m')}-01&end_date={yesterday.strftime('%Y-%m')}-30"
        )
        response = client.get(
            f"/api/daily-species/?start_date={yesterday.strftime('%Y-%m')}-01&end_date={yesterday.strftime('%Y-%m')}-30"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), len(species_today))

    @skipIf(
        (settings.FLICKR_KEY is None), "Skip this if Flickr credentials are not set."
    )
    def test_flickr_unmocked(self):
        species = app_models.Species.objects.create(
            common_name="American Crow", scientific_name="Corvus brachyrhynchos"
        )
        # print(species)
        client = APIClient()
        response = client.get(f"/api/species/{species.id}/image/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("url" in response.json())
        # pprint(response.json())
