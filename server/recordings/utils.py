from recordings.models import Analysis, Recording, Analyzer, Species, Detection
from recordings.models import (
    RECORDING_ANALYZED_STATUS_CHOICES,
    ACQUISITION_TYPE,
    DETECTION_STATUS,
    NOTIFICATION_DETECTION_TYPES,
)
from django.contrib.gis.geos import Point

from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.utils.text import slugify


import tempfile

# import pytz

import apprise
from pydub import AudioSegment
import os


def import_from_recording(rec_obj):
    # Imports from a birdnetlib.Recording object.
    # Make date timezone aware.
    recording_started_at = timezone.make_aware(rec_obj.date)
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
        if settings.DETECTION_EXTRACTION_ENABLED:
            extract_detection_audio_file(detection)

    return recording_obj


def send_notification_for_detection(detection, notification_config):
    print("Sending detection")
    # Create an Apprise instance
    apobj = apprise.Apprise()
    apobj.add(notification_config.apprise_string)

    title = NOTIFICATION_DETECTION_TYPES[notification_config.detection_type]
    body_with_url = f"{detection.species.common_name} - confidence @ {detection.confidence:.2f} http://{settings.DOMAIN}/species/{detection.species.id}/"
    body_without_url = f"{detection.species.common_name} - confidence @ {detection.confidence:.2f}"
    result = apobj.notify(
        body=body_without_url,
        title=f"{title}",
    )


def extract_detection_audio_file(detection):

    if not os.path.exists(detection.recording.filepath):
        return None

    audio = AudioSegment.from_file(detection.recording.filepath)
    start = detection.start_time
    end = detection.end_time
    extract = audio[start * 1000 : end * 1000]  # In milliseconds
    bitrate = settings.DETECTION_EXTRACTION_BITRATE

    if detection.detected_at:
        dt = detection.detected_at
        date_str = dt.strftime("%Y%d%m-%Hh%Mm%Ss")
        filename = f"{detection.species.common_name}-{date_str}"
    else:
        filename = f"{detection.species.common_name}-undated-{detection.id:07}"

    filename = slugify(filename)

    # Make tempfile for pydub and export extraction.
    with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
        extracted_path = tmp.name
        extract.export(extracted_path, format="mp3", bitrate=f"{bitrate}k")

        # Save extracted file to Django.
        with open(extracted_path, mode="rb") as file:
            detection.extracted_file.save(f"{filename}.mp3", file)

    detection.extracted = True
    detection.save()
