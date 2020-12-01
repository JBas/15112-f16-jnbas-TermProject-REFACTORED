import scipy.signal
import numpy as np
import wave
import pyaudio

import matplotlib.pyplot as plt

import struct

class Audio():

    RATE = 44100
    CHANNELS = 2
    FORMAT = pyaudio.paInt16
    CHUNK = 1024

    p = pyaudio.PyAudio()

    def record():
        stream = Audio.p.open(Audio.RATE,
                              Audio.CHANNELS,
                              Audio.FORMAT,
                              input=True,
                              frames_per_buffer=Audio.CHUNK)

        frames = []
        for i in range(Audio.RATE//Audio.CHUNK * 5):
            frames.append(stream.read(Audio.CHUNK))
        stream.stop_stream()
        stream.close()
        return frames

    def display():
        frames = Audio.record()
#        obj = wave.open('sound.wav','wb')
#        obj.setnchannels(Audio.CHANNELS)
#        obj.setsampwidth(Audio.p.get_sample_size(Audio.FORMAT))
#        obj.setframerate(Audio.RATE)
#        obj.writeframes(b''.join(frames))
#        obj.close()

        time = np.asarray(range(Audio.RATE//Audio.CHUNK * 5))

        # @TODO: trouble parsing data
        amplitude = np.asarray(struct.unpack("{}h".format(Audio.CHUNK*2*len(frames)),
                                b''.join(frames)))
        fig, ax = plt.subplots()
        ax.plot(time, amplitude)
        plt.show()

        return

    def close():
        Audio.p.terminate()
        return
