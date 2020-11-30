#import scipy.signal
#import numpy as np
#import wave
#import pyaudio
import pyglet

WIDTH = 600
HEIGHT = 400

window = pyglet.window.Window(width=WIDTH,
                              height=HEIGHT,
                              caption="Term Project -- Refactored",
                              resizable=False)

@window.event
def on_draw():
    window.clear()

pyglet.app.run()
