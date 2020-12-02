import time
import threading
from scipy import signal
import numpy as np
import wave
import pyaudio

import matplotlib.pyplot as plt



class Audio():

    RATE = 44100
    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    CHUNK = 1024

    p = pyaudio.PyAudio()

    BUFFERS = []
    BUFFERS_PRODUCE = threading.Semaphore(10) # available space to produce
    BUFFERS_CONSUME = threading.Semaphore(0) # available data to consume

    STOPEVENT = threading.Event()

    def record(type="threaded", seconds=0):
        if (type == "timed"):
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
        elif (type == "callback"):
            Audio.callback_record()
            return
        elif (type == "threaded"):
            t = threading.Thread(target=Audio.thread_record, name="producer")
            t.start()
            fig, ax = plt.subplots()
            t1 = threading.Thread(target=Audio.filter, name="consumer", args=(fig, ax))
            t1.start()
            plt.show()
            return

    def callback_record():

        def callback(in_data, frame_count, time_info, status):
            data = np.fromstring(in_data, dtype=np.int16)
            b, a = signal.butter(4, 0.1, analog=False, fs=Audio.RATE)
            filtered = signal.filtfilt(b, a, data)
            print(filtered)
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

    def thread_record():
        stream = Audio.p.open(Audio.RATE,
                              Audio.CHANNELS,
                              Audio.FORMAT,
                              input=True,
                              frames_per_buffer=Audio.CHUNK)

        while (not Audio.STOPEVENT.is_set()):
            # produce
            buffer = stream.read(Audio.CHUNK)

            Audio.BUFFERS_PRODUCE.acquire()
            Audio.BUFFERS.append(buffer)
            Audio.BUFFERS_CONSUME.release()
        return

    def filter(fig, ax):
        while (True):
            Audio.BUFFERS_CONSUME.acquire()
            buffer = Audio.BUFFERS.pop(0)
            Audio.BUFFERS_PRODUCE.release()

            #consume
            data = np.fromstring(buffer, dtype=np.int16)
            ax.clear()
            ax.imshow(data)
            fig.canvas.draw_idle()



    def display(seconds):
        buffers = Audio.record(seconds)

        time = np.arange(Audio.RATE//Audio.CHUNK * seconds)
        # channel are interleaved and not separable (?)
        # so can't really show interesting data with multiple channels
        amplitude = np.fromstring(buffers, dtype=np.int16)
        time = np.arange(len(amplitude)) / Audio.RATE
        b, a = signal.butter(1, 100, analog=False, fs=Audio.RATE)
        filtered = signal.filtfilt(b, a, amplitude)
        fig, ax = plt.subplots()
        ax.plot(time, amplitude)
        plt.show()
        return

    def close():
        if (not Audio.STOPEVENT.is_set()):
            Audio.STOPEVENT.set()
        Audio.p.terminate()
        return
