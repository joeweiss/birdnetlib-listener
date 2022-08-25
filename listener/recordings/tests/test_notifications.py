from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from recordings.models import (
    Analysis,
    Analyzer,
    Recording,
    RECORDING_ANALYZED_STATUS_CHOICES,
    ACQUISITION_TYPE,
    NotificationConfig,
    NOTIFICATION_DETECTION_TYPES,
    NOTIFICATION_TYPES,
    Species,
    Detection,
)
from django.contrib.gis.geos import Point
from recordings.utils import import_from_recording
from mock import patch, Mock


class NotifactionsTestCase(TestCase):
    def setUp(self):
        self.analyzer = Analyzer.objects.create(name="Default Analyzer")
        self.recording = Recording.objects.create(recording_started=timezone.now())
        self.analysis = Analysis.objects.create(
            recording=self.recording, analyzer=self.analyzer
        )
        self.species = Species.objects.create(
            common_name="Yellow-billed Cuckoo", scientific_name="Coccyzus americanus"
        )

    def test_all_type_notifications(self):
        # No notification sent.
        with patch("recordings.utils.send_notification_for_detection") as mock_nofity:
            detection = Detection.objects.create(
                recording=self.recording,
                species=self.species,
                analyzer=self.analyzer,
                analysis=self.analysis,
                detected_at=self.recording.recording_started,
                confidence=0.99,
            )
            self.assertEqual(mock_nofity.call_count, 0)

            # Add config, expect 1 notification.

            config = NotificationConfig.objects.create(
                name="Joe's config",
                apprise_string="twilio://...",
                detection_type=NOTIFICATION_DETECTION_TYPES.all,
            )
            detection = Detection.objects.create(
                recording=self.recording,
                species=self.species,
                analyzer=self.analyzer,
                analysis=self.analysis,
                detected_at=self.recording.recording_started,
                confidence=0.99,
            )
            self.assertEqual(mock_nofity.call_count, 1)

    def test_new_daily_type_notifications(self):
        # No notification sent.
        with patch("recordings.utils.send_notification_for_detection") as mock_nofity:

            # Add config, expect 1 notification.
            config = NotificationConfig.objects.create(
                name="Joe's config",
                apprise_string="twilio://...",
                detection_type=NOTIFICATION_DETECTION_TYPES.new_daily,
            )

            # Add detection many days ago.
            detection = Detection.objects.create(
                recording=self.recording,
                species=self.species,
                analyzer=self.analyzer,
                analysis=self.analysis,
                detected_at=timezone.now() - timedelta(days=14),
                confidence=0.99,
            )
            self.assertEqual(mock_nofity.call_count, 0)

            detection = Detection.objects.create(
                recording=self.recording,
                species=self.species,
                analyzer=self.analyzer,
                analysis=self.analysis,
                detected_at=self.recording.recording_started,
                confidence=0.99,
            )
            self.assertEqual(mock_nofity.call_count, 1)

            # Second detection, should not trigger send.
            detection = Detection.objects.create(
                recording=self.recording,
                species=self.species,
                analyzer=self.analyzer,
                analysis=self.analysis,
                detected_at=self.recording.recording_started,
                confidence=0.99,
            )
            self.assertEqual(mock_nofity.call_count, 1)

    def test_new_alltime_type_notifications(self):
        # No notification sent.
        with patch("recordings.utils.send_notification_for_detection") as mock_nofity:

            # Add config, expect 1 notification.
            config = NotificationConfig.objects.create(
                name="Joe's config",
                apprise_string="twilio://...",
                detection_type=NOTIFICATION_DETECTION_TYPES.new_all_time,
            )
            detection = Detection.objects.create(
                recording=self.recording,
                species=self.species,
                analyzer=self.analyzer,
                analysis=self.analysis,
                detected_at=timezone.now() - timedelta(days=14),
                confidence=0.99,
            )
            self.assertEqual(mock_nofity.call_count, 1)

            # Second detection, should not trigger send.
            detection = Detection.objects.create(
                recording=self.recording,
                species=self.species,
                analyzer=self.analyzer,
                analysis=self.analysis,
                detected_at=timezone.now(),
                confidence=0.99,
            )
            self.assertEqual(mock_nofity.call_count, 1)
