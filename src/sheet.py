import pyglet

class Sheet(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.batch = pyglet.graphics.Batch()

        title = pyglet.text.Label("Title",
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=self.width//2, y=self.height,
                                  anchor_x="center", anchor_y="top",
                                  color=(0, 0, 0, 255), batch=self.batch)
        line = pyglet.shapes.Line(0, self.height//2, self.width, self.height//2, width=1, batch=self.batch)

        pass

    def loadAssets():
        pass

    def on_draw(self):
        self.clear()
        self.batch.draw()
