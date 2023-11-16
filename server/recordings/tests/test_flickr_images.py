from django.test import TestCase
from unittest import skipIf
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from recordings import models as app_models
from pprint import pprint
from django.conf import settings

User = get_user_model()


# watchmedo shell-command -c "python manage.py test recordings.tests.test_api --failfast --keepdb" --recursive -W


class FlickrImagesTestCase(TestCase):
    @skipIf(
        (settings.FLICKR_KEY is None), "Skip this if Flickr credentials are not set."
    )
    def test_flickr_unmocked(self):
        print("test_flickr_unmocked")
        species = app_models.Species.objects.create(
            common_name="American Crow", scientific_name="Corvus brachyrhynchos"
        )
        # print(species)
        client = APIClient()
        response = client.get(f"/api/species/{species.id}/image/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("url" in response.json())
        self.assertEqual(app_models.SpeciesImage.objects.count(), 1)
        species_image = app_models.SpeciesImage.objects.first()
        self.assertEqual(species_image.species, species)
        self.assertEqual(species_image.is_active, True)

        # Patch to hide.
        response = client.patch(
            f"/api/species-images/{species_image.id}/", data={"is_active": False}
        )

        print(response.json())
        species_image = app_models.SpeciesImage.objects.first()
        self.assertEqual(species_image.is_active, False)

        # pprint(response.json())
