import time
import scipy.signal
import numpy as np
import wave
import pyaudio

import matplotlib.pyplot as plt

class Audio():

    RATE = 44100
    CHANNELS = 2
    FORMAT = pyaudio.paInt16
    CHUNK = 1024

    p = pyaudio.PyAudio()

    def record(seconds):
        stream = Audio.p.open(Audio.RATE,
                              Audio.CHANNELS,
                              Audio.FORMAT,
                              input=True,
                              frames_per_buffer=Audio.CHUNK)

        buffers = []
        for i in range(Audio.RATE//Audio.CHUNK * seconds):
            buffers.append(stream.read(Audio.CHUNK))
        stream.stop_stream()
        stream.close()
        return b''.join(buffers)

    def callback_record():

        def callback(in_data, frame_count, time_info, status):

            return (None, pyaudio.paContinue)

        stream = Audio.p.open(Audio.RATE,
                              Audio.CHANNELS,
                              Audio.FORMAT,
                              input=True,
                              frames_per_buffer=Audio.CHUNK,
                              stream_callback=callback)

        stream.start_stream()
        while stream.is_active():
            pass
        stream.stop_stream()
        stream.close()
        return

    def display(seconds):
        buffers = Audio.record(seconds)

        time = np.asarray(range(Audio.RATE//Audio.CHUNK * seconds))

        # channel are interleaved and not separable (?)
        # so can't really show interesting data with multiple channels
        amplitude = np.fromstring(buffers, dtype=np.int16)
        fig, ax = plt.subplots()
        ax.plot(amplitude)
        plt.show()
        return

    def close():
        Audio.p.terminate()
        return
