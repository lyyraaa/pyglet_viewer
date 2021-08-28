import pyglet

window = pyglet.window.Window(640, 480, resizable=True, vsync=True)
batch = pyglet.graphics.Batch()

@window.event
def on_draw():
    window.clear()
    batch.draw()

from pyglet_gui.theme import Theme

theme = Theme({"font": "Lucida Grande",
               "font_size": 12,
               "text_color": [255, 0, 0, 255]}, resources_path='')

from pyglet_gui.gui import Label

label = Label('Hello world')

from pyglet_gui.manager import Manager

Manager(label, window=window, theme=theme, batch=batch)

pyglet.app.run()
