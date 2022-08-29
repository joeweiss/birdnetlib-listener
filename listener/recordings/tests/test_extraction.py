from django.test import TestCase
from django.utils import timezone
from recordings.models import (
    Analysis,
    Analyzer,
    Recording,
    Species,
    Detection,
)
import shutil
import os
from recordings.utils import extract_detection_audio_file


class ExtractionTestCase(TestCase):
    def setUp(self):
        self.analyzer = Analyzer.objects.create(name="Default Analyzer")
        self.recording = Recording.objects.create(recording_started=timezone.now())
        self.analysis = Analysis.objects.create(
            recording=self.recording, analyzer=self.analyzer
        )
        self.species = Species.objects.create(
            common_name="Yellow-billed Cuckoo", scientific_name="Coccyzus americanus"
        )
        self.detection = Detection(
            recording=self.recording,
            species=self.species,
            analyzer=self.analyzer,
            analysis=self.analysis,
            confidence=0.9,
            detected_at=timezone.now(),
            start_time=0,
            end_time=3,
        )
        self.archive_dir = "recordings/tests/files/archives"
        try:
            shutil.rmtree(self.archive_dir)
        except:
            pass
        os.mkdir(self.archive_dir)

    def tearDown(self):
        shutil.rmtree(self.archive_dir)

    def test_extraction(self):

        with self.settings(
            DETECTION_EXTRACTION_DIRECTORY=self.archive_dir, MEDIA_ROOT=self.archive_dir
        ):
            path = "recordings/tests/files/audio.wav"
            self.recording.filepath = path
            self.recording.save()
            extract_detection_audio_file(self.detection)

            self.detection.refresh_from_db()

            self.assertTrue(self.detection.extracted)

            self.assertIsNotNone(self.detection.extracted_file)
            self.assertTrue(os.path.exists(self.detection.extracted_file.path))

            # Clean up files
            self.detection.extracted_file.delete()

    def test_extraction_no_date(self):

        with self.settings(
            DETECTION_EXTRACTION_DIRECTORY=self.archive_dir, MEDIA_ROOT=self.archive_dir
        ):
            path = "recordings/tests/files/audio.wav"
            self.recording.filepath = path
            self.recording.save()

            self.detection.detected_at = None
            self.detection.save()

            extract_detection_audio_file(self.detection)

            self.detection.refresh_from_db()

            self.assertTrue(self.detection.extracted)

            self.assertIsNotNone(self.detection.extracted_file)
            self.assertTrue(os.path.exists(self.detection.extracted_file.path))

            # Clean up files
            self.detection.extracted_file.delete()
