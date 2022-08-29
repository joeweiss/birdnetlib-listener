# https://swharden.com/blog/2016-07-19-realtime-audio-visualization-in-python/

import pyaudio
import numpy as np
import wave

CHUNK = 1024
print(CHUNK)
RATE = 44100

duration = 10

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i, dev["name"], dev["maxInputChannels"]))

p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16, channels=2, rate=RATE, input=True, frames_per_buffer=CHUNK
)

frames = []  # Initialize array to store frames

for i in range(int(duration * 44100 / 1024)):  # go for a few seconds
    frame_data = stream.read(CHUNK)
    frames.append(frame_data)
    data = np.frombuffer(frame_data, dtype=np.int16)
    peak = np.average(np.abs(data)) * 2
    bars = "#" * int(50 * peak / 2**16)
    print("%04d %05d %s" % (i, peak, bars))


stream.stop_stream()
stream.close()
p.terminate()

print("Finished recording")

# Save the recorded data as a WAV file
filename = "output.wav"
channels = 2
sample_format = pyaudio.paInt16  # 16 bits per sample
fs = 44100

wf = wave.open(filename, "wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b"".join(frames))
wf.close()
