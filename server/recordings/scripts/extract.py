from recordings.models import Detection
from recordings.utils import extract_detection_audio_file


def run():
    unextracted_detections = Detection.objects.all().filter(extracted=False)
    for d in unextracted_detections:
        print(d)
        extract_detection_audio_file(d)
