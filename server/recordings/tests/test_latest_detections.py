from django.test import TestCase
from collections import namedtuple

from django.utils import timezone
from datetime import datetime, timedelta

from recordings.models import (
    Recording,
    RECORDING_ANALYZED_STATUS_CHOICES,
    ACQUISITION_TYPE,
    Detection,
)
from django.contrib.gis.geos import Point
from recordings.utils import import_from_recording
from django.urls import reverse
from pprint import pprint


class DetectionsTestCase(TestCase):
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

        naive_datetime = timezone.now()

        recording = BirdnetlibRecording(
            "recordings/tests/files/audio.wav",
            analyzer,
            detections,
            naive_datetime,
            -77.3664,
            35.6127,
            0.1,
        )
        # print(recording)

        recording_obj = Recording.objects.create(
            recording_started=recording.date,
            location=Point(recording.lon, recording.lat),
            has_accurate_location=True,
            filepath=recording.path,
            analyze_status=RECORDING_ANALYZED_STATUS_CHOICES.pending,
            acquistion_type=ACQUISITION_TYPE.automated,
        )
        # print(recording_obj)
        self.assertEqual(recording_obj.id > 0, True)

    def test_ingest_from_recording_object(self):
        detections = [
            {
                "common_name": "Gray Catbird",
                "confidence": 0.9,
                "end_time": 3.0,
                "scientific_name": "Cathartes aura",
                "start_time": 0.0,
            },
            {
                "common_name": "Northern Cardinal",
                "confidence": 0.9,
                "end_time": 9.0,
                "scientific_name": "Cathartes aura",
                "start_time": 6.0,
            },
            {
                "common_name": "Turkey Vulture",
                "confidence": 0.9,
                "end_time": 15.0,
                "scientific_name": "Cathartes aura",
                "start_time": 12.0,
            },
            {
                "common_name": "Turkey Vulture",
                "confidence": 0.9,
                "end_time": 18.0,
                "scientific_name": "Cathartes aura",
                "start_time": 15.0,
            },
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

        naive_datetime = datetime.utcnow() - timedelta(hours=0, minutes=1)
        print(naive_datetime)

        recording = BirdnetlibRecording(
            "recordings/tests/files/audio.wav",
            analyzer,
            detections,
            naive_datetime,
            -77.3664,
            35.6127,
            0.1,
        )
        # print(recording)

        rec_obj = import_from_recording(recording)
        self.assertEqual(rec_obj.recording_started, timezone.make_aware(naive_datetime))
        # print("rec_obj", rec_obj)
        self.assertEqual(rec_obj.id > 0, True)

        detections = Detection.objects.all().filter(recording=rec_obj)
        print(detections)

        # Make a GET request to the "latest" URL
        response = self.client.get(reverse("recordings:latest"))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response content type is JSON
        self.assertEqual(response["Content-Type"], "application/json")

        data = response.json()
        pprint(data)

        self.assertEqual(data["daily_count"], 3)
        self.assertEqual(
            data["last_minute"], ["Turkey Vulture", "Northern Cardinal", "Gray Catbird"]
        )
        self.assertEqual(
            data["last_hour"], ["Turkey Vulture", "Northern Cardinal", "Gray Catbird"]
        )
        self.assertEqual(data["most_common"], ["Turkey Vulture"])
        pprint(response.json())
