import pyglet
from pyglet.shapes import Line
import json

class Staff():

    __LINES = 5
    __LINE_WIDTH = 1
    __LINE_SPACE = 5

    def __init__(self, x, y, width, batch=None):
        self.__width = width
        self.__x = x # horizontally centered
        self.__y = y # from top
        self.__batch = batch

        self.__lines = []
        for i in range(Staff.__LINES):
            self.__lines.append(Line(x, y - i*Staff.__LINE_SPACE, x+width, y - i*Staff.__LINE_SPACE, color=(0, 0, 0), batch=self.__batch))


class Sheet(pyglet.window.Window):

    __LOADED = False

    __BASE_NOTES = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if (not Sheet.__LOADED):
            with open("notes.json") as f:
                Sheet.__BASE_NOTES = json.load(f)
            Sheet.__LOADED = True

        self.batch = pyglet.graphics.Batch()

        title = pyglet.text.Label("Title",
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=self.width//2, y=self.height,
                                  anchor_x="center", anchor_y="top",
                                  color=(0, 0, 0, 255), batch=self.batch)

        self.notes = []

        self.staff = Staff(50, self.height//2, self.width//3, batch=self.batch)

        pass

    def addNote(note):
        self.notes.append(note)

    def loadAssets():
        pass

    def on_draw(self):
        self.clear()
        self.batch.draw()
