from django.test import TestCase
from collections import namedtuple

from datetime import datetime

from recordings.models import (
    Recording,
    RECORDING_ANALYZED_STATUS_CHOICES,
    ACQUISITION_TYPE,
)
from django.contrib.gis.geos import Point
from recordings.utils import import_from_recording


class BirdnetlibTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_recording_object(self):

        detections = [
            {
                "common_name": "Turkey Vulture",
                "confidence": 0.12117741,
                "end_time": 15.0,
                "scientific_name": "Cathartes aura",
                "start_time": 12.0,
            }
        ]
        BirdnetlibRecording = namedtuple(
            "Recording",
            [
                "path",
                "analyzer",
                "detections",
                "date",
                "lon",
                "lat",
                "minimum_confidence",
            ],
        )
        Analyzer = namedtuple("Analyzer", ["name", "model_name"])
        analyzer = Analyzer("Analyzer", "BirdNET-Analyzer")

        naive_datetime = datetime.now()

        recording = BirdnetlibRecording(
            "recordings/tests/files/audio.wav",
            analyzer,
            detections,
            naive_datetime,
            -77.3664,
            35.6127,
            0.1,
        )
        print(recording)

        recording_obj = Recording.objects.create(
            recording_started=recording.date,
            location=Point(recording.lon, recording.lat),
            has_accurate_location=True,
            filepath=recording.path,
            analyze_status=RECORDING_ANALYZED_STATUS_CHOICES.pending,
            acquistion_type=ACQUISITION_TYPE.automated,
        )
        print(recording_obj)
        self.assertEqual(recording_obj.id > 0, True)

    def test_ingest_from_recording_object(self):

        detections = [
            {
                "common_name": "Turkey Vulture",
                "confidence": 0.12117741,
                "end_time": 15.0,
                "scientific_name": "Cathartes aura",
                "start_time": 12.0,
            }
        ]

        BirdnetlibRecording = namedtuple(
            "Recording",
            [
                "path",
                "analyzer",
                "detections",
                "date",
                "lon",
                "lat",
                "minimum_confidence",
            ],
        )
        Analyzer = namedtuple("Analyzer", ["name", "model_name"])
        analyzer = Analyzer("Analyzer", "BirdNET-Analyzer")

        naive_datetime = datetime.now()

        recording = BirdnetlibRecording(
            "recordings/tests/files/audio.wav",
            analyzer,
            detections,
            naive_datetime,
            -77.3664,
            35.6127,
            0.1,
        )
        print(recording)

        rec_obj = import_from_recording(recording)
        print("rec_obj", rec_obj)
        self.assertEqual(rec_obj.id > 0, True)
