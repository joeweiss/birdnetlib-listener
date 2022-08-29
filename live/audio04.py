# https://swharden.com/blog/2016-07-19-realtime-audio-visualization-in-python/

import pyaudio
import numpy as np
import wave
from threading import Thread
from time import sleep
import sys

print(sys.maxsize**10)  # You can use this as the max duration if needed.


CHUNK = 1024
print(CHUNK)
RATE = 44100

duration = 10

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

    for i in range(int(duration * 44100 / 1024)):  # go for a few seconds
        frame_data = stream.read(CHUNK)
        frames.append(frame_data)
        d = (
            np.frombuffer(frame_data, dtype=np.int16).astype(np.float32, order="C")
            / 32768.0
        )
        print(d)
        data.append(d)
        # print(data[0])
        # peak = np.average(np.abs(data)) * 2
        # bars = "#" * int(50 * peak / 2**16)
        # # print("%04d %05d %s" % (i, peak, bars))

    stream.stop_stream()
    stream.close()
    p.terminate()


print("Finished recording")


def save():
    counter = 0
    while True:
        sleep(2)
        # Save the recorded data as a WAV file
        filename = f"output_{counter}.wav"
        channels = 1
        sample_format = pyaudio.paInt16  # 16 bits per sample
        fs = 44100
        wf = wave.open(filename, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)

        global frames
        _frames = frames.copy()
        frames = []

        wf.writeframes(b"".join(_frames))
        wf.close()
        counter = counter + 1


Thread(target=record).start()
Thread(target=save).start()
