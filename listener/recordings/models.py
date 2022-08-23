from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from model_utils.models import TimeStampedModel
from model_utils import Choices

RECORDING_ANALYZED_STATUS_CHOICES = Choices(
    ("analyzed", "Analyzed"), ("pending", "Pending"), ("ignored", "Ignored")
)


class Recording(models.Model):
    recording_started = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Time when recording was started (Timezone aware)",
    )
    duration = models.DurationField(null=True, blank=True)
    location = PointField(geography=True, default=Point(0.0, 0.0))
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    analyze_status = models.CharField(
        max_length=30,
        choices=RECORDING_ANALYZED_STATUS_CHOICES,
        default=RECORDING_ANALYZED_STATUS_CHOICES.pending,
    )

    @property
    def longitude(self):
        return self.location.x

    @property
    def latitude(self):
        return self.location.y


class Species(models.Model):
    common_name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "species"


class Analyzer(TimeStampedModel):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    release_date = models.DateTimeField()


DETECTION_STATUS = Choices(
    ("automated_detection_only", "Automated detection only"),
    ("reviewed_valid", "Human reviewed as valid"),
    ("reviewed_invalid", "Human reviewed as invalid"),
)


class Detection(models.Model):
    recording = models.ForeignKey(to=Recording, on_delete=models.CASCADE)
    species = models.ForeignKey(to=Species, on_delete=models.CASCADE)
    analyzer = models.ForeignKey(to=Analyzer, on_delete=models.CASCADE)
    confidence = models.FloatField(default=0.0)
    start_time = models.FloatField(blank=True, null=True, help_text="Time in seconds")
    end_time = models.FloatField(blank=True, null=True, help_text="Time in seconds")
    status = models.CharField(
        max_length=30,
        choices=DETECTION_STATUS,
        default=DETECTION_STATUS.automated_detection_only,
    )
