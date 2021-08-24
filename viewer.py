import pyglet
from pyglet.window import key
from pyglet.gl import *

window = pyglet.window.Window()

#https://en.wikipedia.org/wiki/Lorenz_system
class Lorenz():
    def __init__(self,x,y,z,dt):
        self.x = x
        self.y = y
        self.z = z

        self.dx = 0
        self.dy = 0
        self.dz = 0

        self.dt = dt

        self.rho = 28
        self.beta = 8/3
        self.sigma = 10

    def step(self):
        deltax = self.dt * (self.sigma * (self.y-self.x))
        deltay = self.dt * (self.x * (self.rho - self.z) - self.y)
        deltaz = self.dt * (self.x * self.y - self.beta * self.z)

        self.x += deltax
        self.y += deltay
        self.z += deltaz

    def get_location(self):
        return (self.x,self.y,self.z)

    def get_velocity(self):
        return (self.dx,self.dy,self.dz)

lorenz = Lorenz(0.01,0.01,0.01,0.01)

STEPS = 10000
SCALE = 1

line_coords = [0]*(STEPS*3)
for step in range(STEPS):
    stepoffset = step*3
    line_coords[stepoffset],line_coords[stepoffset+1],line_coords[stepoffset+2] = [coord*SCALE for coord in lorenz.get_location()]
    lorenz.step()

line = pyglet.graphics.vertex_list(STEPS, 'v3f/static', 'c3B/static')
line.vertices = line_coords
line.colors = [255]*3*STEPS
line.draw(pyglet.gl.GL_LINE_STRIP)

###################################################################################


def update(dt):
    move(keys)

@window.event
def on_draw():
    window.clear()
    line.draw(pyglet.gl.GL_LINE_STRIP)


# for finding out what is being pressed
#event_logger = pyglet.window.event.WindowEventLogger()
#window.push_handlers(event_logger)
pos = [0,0,0]
state = False
# xyz
# w,s affect z axis
# a,d affect x
# space ctrl affect y

def move(keys):
    unit = 1
    if keys[key.W]:
        glTranslatef(0,0,unit)
        pos[2] += unit
    if keys[key.S]:
        glTranslatef(0,0,-unit)
        pos[2] -= unit
    if keys[key.A]:
        glTranslatef(unit,0,0)
        pos[0] += unit
    if keys[key.D]:
        glTranslatef(-unit,0,0)
        pos[0] -= unit
    if keys[key.SPACE]:
        glTranslatef(0,-unit,0)
        pos[1] -= unit
    if keys[key.LCTRL]:
        glTranslatef(0,unit,0)
        pos[1] += unit

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        window.close()
    if symbol == key.E:
        window.set_exclusive_mouse(True)
    if symbol == key.R:
        window.set_exclusive_mouse(False)



@window.event
def on_mouse_motion(x,y,dx, dy):
    glTranslatef(-pos[0],-pos[1],-pos[2])
    glRotatef(1, -dy, dx, 0)
    glTranslatef(pos[0],pos[1],pos[2])


glClearColor(.1,.1,.1,1)
window.projection = pyglet.window.Projection3D()
keys = key.KeyStateHandler()
window.push_handlers(keys)
dir(window)
window.set_exclusive_mouse(False)
pyglet.clock.schedule_interval(update,1/60)
pyglet.app.run()
