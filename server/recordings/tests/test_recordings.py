import tempfile
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
import tempfile
import shutil
import os


class RecordingsTestCase(TestCase):
    def setUp(self):
        self.analyzer = Analyzer.objects.create(name="Default Analyzer")
        self.recording = Recording.objects.create(recording_started=timezone.now())
        self.analysis = Analysis.objects.create(
            recording=self.recording, analyzer=self.analyzer
        )
        self.species = Species.objects.create(
            common_name="Yellow-billed Cuckoo", scientific_name="Coccyzus americanus"
        )
        self.archive_dir = "recordings/tests/files/archives"
        try:
            os.rmdir(self.archive_dir)
        except:
            pass
        os.mkdir(self.archive_dir)

    def tearDown(self):
        os.rmdir(self.archive_dir)

    def test_recording_archive_file(self):

        with self.settings(OUTPUT_WAV_FILE_DIRECTORY=self.archive_dir):
            path = "recordings/tests/files/audio.wav"
            tmp = tempfile.NamedTemporaryFile(delete=True, suffix=".wav")
            filename = os.path.basename(tmp.name)
            shutil.copy2(path, tmp.name)

            self.recording.filepath = tmp.name
            self.recording.save()

            self.recording.archive_file()

            self.recording.refresh_from_db()

            self.assertEqual(self.recording.filepath, f"{self.archive_dir}/{filename}")

            # Assert file new positions.
            self.assertFalse(os.path.exists(tmp.name))
            self.assertTrue(os.path.exists(self.recording.filepath))

            # Copy back to prevent exception.
            shutil.move(self.recording.filepath, tmp.name)

    def test_recording_delete_file(self):

        with self.settings(OUTPUT_WAV_FILE_DIRECTORY=self.archive_dir):
            path = "recordings/tests/files/audio.wav"
            tmp = tempfile.NamedTemporaryFile(delete=True, suffix=".wav")
            shutil.copy2(path, tmp.name)

            self.recording.filepath = tmp.name
            self.recording.save()

            self.recording.delete_file()

            self.recording.refresh_from_db()

            self.assertTrue(self.recording.is_deleted)
            self.assertEqual(self.recording.filepath, None)

            # Assert not at old filepath.
            self.assertFalse(os.path.exists(tmp.name))

            # Copy back to prevent exception.
            shutil.copy2(path, tmp.name)
