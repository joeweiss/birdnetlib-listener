from recordings.models import Analysis, Recording, Analyzer, Species, Detection
from recordings.models import (
    RECORDING_ANALYZED_STATUS_CHOICES,
    ACQUISITION_TYPE,
    DETECTION_STATUS,
)
from django.contrib.gis.geos import Point
# from django.conf import settings
from datetime import timedelta
from django.utils import timezone
# import pytz


def import_from_recording(rec_obj):
    # Imports from a birdnetlib.Recording object.
    recording_started_at = timezone.make_aware(rec_obj.date)
    # recording_started_at = timezone.localtime(
    #     rec_obj.date, pytz.timezone(settings.TIME_ZONE)
    # )
    recording_obj, created = Recording.objects.get_or_create(
        recording_started=recording_started_at,
        filepath=rec_obj.path,
        analyze_status=RECORDING_ANALYZED_STATUS_CHOICES.analyzed,
        acquistion_type=ACQUISITION_TYPE.automated,
    )

    if rec_obj.lon and rec_obj.lat:
        recording_obj.location = Point(rec_obj.lon, rec_obj.lat)
        recording_obj.has_accurate_location = True
        recording_obj.save()

    analyzer, created = Analyzer.objects.get_or_create(name=rec_obj.analyzer.name)
    analysis = Analysis.objects.create(analyzer=analyzer, recording=recording_obj)

    for d in rec_obj.detections:
        detection = Detection()
        detection.recording = recording_obj
        species_obj, created = Species.objects.get_or_create(
            scientific_name=d["scientific_name"], common_name=d["common_name"]
        )
        detection.species = species_obj
        detection.analyzer = analyzer
        detection.analysis = analysis
        detection.confidence = d["confidence"]
        detection.start_time = d["start_time"]
        detection.end_time = d["end_time"]
        if recording_obj.recording_started:
            detection.detected_at = recording_obj.recording_started + timedelta(
                seconds=detection.start_time
            )
        detection.status = DETECTION_STATUS.automated_detection_only
        detection.save()

    return recording_obj
