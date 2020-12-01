#import audio
from sheet import Sheet
import pyglet

WIDTH = 600
HEIGHT = 400

sheet = Sheet(width=WIDTH,
              height=HEIGHT,
              caption="Term Project -- Refactored",
              resizable=False)

pyglet.gl.glClearColor(255, 255, 255, 1)

pyglet.app.run()
