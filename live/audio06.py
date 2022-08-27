# https://swharden.com/blog/2016-07-19-realtime-audio-visualization-in-python/

import pyaudio
import numpy as np
import wave
from threading import Thread
from time import sleep
import sys
from pprint import pprint
import struct
from datetime import datetime

import scipy.io.wavfile as wav

from birdnetlib.analyzer import Analyzer
from birdnetlib import Recording
from collections import namedtuple

print(sys.maxsize**10)  # You can use this as the max duration if needed.


CHUNK = 1024
print(CHUNK)
RATE = 48000

duration = 30

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i, dev["name"], dev["maxInputChannels"]))


global frames
frames = []  # Initialize array to store frames
global data
data = []


def record():

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    for i in range(int(duration * 48000 / 1024)):  # go for a few seconds
        frame_data = stream.read(CHUNK)
        frames.append(frame_data)
        d = (
            np.frombuffer(frame_data, dtype=np.int16).astype(np.float32, order="C")
            / 32768.0
        )
        # print(d)
        data.append(d)

    stream.stop_stream()
    stream.close()
    p.terminate()


record()

# print(len(data))
# nframes = len(frames)
# out = struct.unpack_from("%dh" % nframes * 1, frames)
# mono = np.array(out)

# scaled = data / 32768

# Convert the list of numpy-arrays into a 1D array (column-wise)
numpydata = np.hstack(data)


seconds = 3
overlap = 0
rate = 48000
minlen = 1.5
chunks = []
for i in range(0, len(numpydata), int((seconds - overlap) * rate)):
    split = numpydata[i : i + int(seconds * rate)]

    # End of signal?
    if len(split) < int(minlen * rate):
        break

    # Signal chunk too short? Fill with zeros.
    if len(split) < int(rate * seconds):
        temp = np.zeros((int(rate * seconds)))
        temp[: len(split)] = split
        split = temp

    chunks.append(split)


class Recording:
    def __init__(self, chunks):
        self.detection_list = []
        self.path = None
        self.sample_secs = 3
        self.chunks = chunks
        self.lon = -77.3664
        self.lat = 35.6127
        self.min_conf = 0.1
        self.overlap = 0
        self.date = datetime.now()
        self.week_48 = 8 * 4


# Recording = namedtuple(
#     "Recording",
#     ["detection_list", "path", "sample_secs", "chunks", "lon", "lat"],
# )

recording = Recording(chunks)


print(recording)
analyzer = Analyzer()
analyzer.analyze_recording(recording)
print(recording.detection_list)
print("Finished recording")

for detection in recording.detection_list:
    print(detection.common_name, detection.scientific_name, detection.confidence)


wav.write("out.wav", rate, numpydata)


# analyzer = LiteAnalyzer()
# recording = Recording(analyzer, "output_0.wav", min_conf=0.1)
# recording.analyze()
# pprint(recording.detections)


# def save():
#     counter = 0
#     while True:
#         sleep(2)
#         # Save the recorded data as a WAV file
#         filename = f"output_{counter}.wav"
#         channels = 1
#         sample_format = pyaudio.paInt16  # 16 bits per sample
#         fs = 48000
#         wf = wave.open(filename, "wb")
#         wf.setnchannels(channels)
#         wf.setsampwidth(p.get_sample_size(sample_format))
#         wf.setframerate(fs)

#         global frames
#         _frames = frames.copy()
#         frames = []

#         wf.writeframes(b"".join(_frames))
#         wf.close()
#         counter = counter + 1


# Thread(target=record).start()
# Thread(target=save).start()
