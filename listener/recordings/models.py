from django.db import models
from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from model_utils.models import TimeStampedModel
from model_utils import Choices

RECORDING_ANALYZED_STATUS_CHOICES = Choices(
    ("analyzed", "Analyzed"), ("pending", "Pending"), ("ignored", "Ignored")
)
ACQUISITION_TYPE = Choices(
    ("manual", "Manual recording"),
    ("automated", "Automated recording"),
    ("third_party", "Third-party recording"),
    ("unknown", "Unknown"),
    ("other", "Other"),
)


class Recording(models.Model):
    recording_started = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Time when recording was started (Timezone aware)",
    )
    duration = models.DurationField(null=True, blank=True)
    location = PointField(geography=True, default=Point(0.0, 0.0))
    has_accurate_location = models.BooleanField(
        default=False, help_text="User confirmed that location data is accurate."
    )
    filepath = models.FilePathField(path=settings.FILE_PATH_FIELD_DIRECTORY)
    analyze_status = models.CharField(
        max_length=30,
        choices=RECORDING_ANALYZED_STATUS_CHOICES,
        default=RECORDING_ANALYZED_STATUS_CHOICES.pending,
    )
    acquistion_type = models.CharField(
        max_length=30,
        choices=ACQUISITION_TYPE,
        default=ACQUISITION_TYPE.unknown,
    )
    is_compressed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    @property
    def longitude(self):
        return self.location.x

    @property
    def latitude(self):
        return self.location.y

    def __str__(self):
        return self.filepath or f"{self.recording_started}"


class Species(models.Model):
    common_name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200)

    def __str__(self):
        return self.common_name

    class Meta:
        verbose_name_plural = "species"


class Analyzer(TimeStampedModel):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20, blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Analysis(TimeStampedModel):
    recording = models.ForeignKey(to=Recording, on_delete=models.CASCADE)
    analyzer = models.ForeignKey(to=Analyzer, on_delete=models.CASCADE)


DETECTION_STATUS = Choices(
    ("automated_detection_only", "Automated detection only"),
    ("reviewed_valid", "Human reviewed as valid"),
    ("reviewed_invalid", "Human reviewed as invalid"),
)


class Detection(models.Model):
    recording = models.ForeignKey(to=Recording, on_delete=models.CASCADE)
    species = models.ForeignKey(to=Species, on_delete=models.CASCADE)
    analyzer = models.ForeignKey(to=Analyzer, on_delete=models.CASCADE)
    analysis = models.ForeignKey(to=Analysis, on_delete=models.CASCADE)
    confidence = models.FloatField(default=0.0)
    detected_at = models.DateTimeField(blank=True, null=True)
    start_time = models.FloatField(blank=True, null=True, help_text="Time in seconds")
    end_time = models.FloatField(blank=True, null=True, help_text="Time in seconds")
    status = models.CharField(
        max_length=30,
        choices=DETECTION_STATUS,
        default=DETECTION_STATUS.automated_detection_only,
    )
