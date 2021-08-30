import pyglet
from pyglet.window import key
from pyglet.gl import *
import math

import pyglet_gui
from pyglet_gui.theme import Theme
from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button
from pyglet_gui.containers import VerticalContainer, HorizontalContainer, Spacer
from pyglet_gui.sliders import HorizontalSlider
from pyglet_gui.gui import Label


from copy import deepcopy



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


###################################################################################
# https://github.com/jjstrydom/pyglet_examples/blob/master/minecraft_block.py
#https://github.com/jorgecarleitao/pyglet-gui/tree/master/examples

class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.initpos = list(pos)
        self.initrot = list(rot)

    def mouse_motion(self, dx, dy):
        dx/= 8
        dy/= 8
        self.rot[0] += dy
        self.rot[1] -= dx
        if self.rot[0]>90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90

    def update(self,dt,keys):
        sens = 0.1
        s = dt*10
        rotY = -self.rot[1]/180*math.pi
        dx, dz = s*math.sin(rotY), math.cos(rotY)
        if keys[key.W]:
            self.pos[0] += dx*sens
            self.pos[2] -= dz*sens
        if keys[key.S]:
            self.pos[0] -= dx*sens
            self.pos[2] += dz*sens
        if keys[key.A]:
            self.pos[0] -= dz*sens
            self.pos[2] -= dx*sens
        if keys[key.D]:
            self.pos[0] += dz*sens
            self.pos[2] += dx*sens
        if keys[key.SPACE]:
            self.pos[1] += s
        if keys[key.LSHIFT]:
            self.pos[1] -= s

    def reset(self):
        print(self.initpos)
        self.pos = self.initpos[:]
        self.rot = self.initrot[:]

class Window3D(pyglet.window.Window):

    def push(self,pos,rot):
        glPushMatrix()
        rot = self.player.rot
        pos = self.player.pos
        glRotatef(-rot[0],1,0,0)
        glRotatef(-rot[1],0,1,0)
        glTranslatef(-pos[0], -pos[1], -pos[2])

    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        self.Projection()
        gluPerspective(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        self.Projection()
        gluPerspective(self.fov, self.width/self.height, 0.05, 1000)
        self.Model()

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    def getPlayer(self):
        return self.player


    lock = False
    mouse_lock = property(lambda self:self.lock, setLock)

    def __init__(self, line, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        self.fov=70

        self.model = line
        self.player = Player((0.5,1.5,1.5),(-30,0))

    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    def on_key_press(self, KEY, _MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock

    def set_fov(self,fov):
        self.fov = fov

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos,self.player.rot)
        self.model.draw(pyglet.gl.GL_LINE_STRIP)
        glPopMatrix()

class WindowUI(pyglet.window.Window):

    def __init__(self, window3D, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window3D = window3D

        self.batch = pyglet.graphics.Batch()

        self.theme = Theme(
            {"font": "Lucida Grande",
            "font_size": 12,
            "text_color": [255, 255, 255, 255],
            "gui_color": [255, 255, 255, 255],
            "button": {
                "text_color": [0, 0, 0, 255],
                "down": {
                    "image": {
                        "source": "button-down.png",
                        "frame": [8, 6, 2, 2],
                        "padding": [18, 18, 8, 6]
                        },
                    },
                "up": {
                    "image": {
                        "source": "button.png",
                        "frame": [6, 5, 6, 3],
                        "padding": [18, 18, 8, 6]
                        }
                    }
                },
            "slider": {
                   "knob": {
                       "image": {
                           "source": "slider-knob.png"
                       },
                       "offset": [-5, -11]
                   },
                   "padding": [8, 8, 8, 8],
                   "step": {
                       "image": {
                           "source": "slider-step.png"
                       },
                       "offset": [-2, -8]
                   },
                   "bar": {
                       "image": {
                           "source": "slider-bar.png",
                           "frame": [8, 8, 8, 0],
                           "padding": [8, 8, 8, 8]
                       }
                   }
               }
            }, resources_path='theme/')

        label_fov = Label('Change FOV')
        label_col = Label('Change Colour')

        button_reset = Button('RESET POS', on_press=self.callback)

        button_col = Button('CHANGE COL', on_press=self.change_col)


        self.sliderFOV = HorizontalSlider(on_set=self.change_fov)

        self.sliderR = HorizontalSlider()
        self.sliderG = HorizontalSlider()
        self.sliderB = HorizontalSlider()

        container_fov = VerticalContainer([label_fov, self.sliderFOV, button_reset])
        container_col = VerticalContainer([label_col, self.sliderR, self.sliderG, self.sliderB, button_col])

        Manager(\
            content=HorizontalContainer([container_fov, Spacer(25), container_col]),
            window=self,
            theme=self.theme,
            batch=self.batch)


    def on_draw(self):
        self.clear()
        self.batch.draw()

    def callback(self,is_pressed):
        self.window3D.set_fov(75)
        self.window3D.getPlayer().reset()

    def change_col(self,is_pressed):
        colvalRGB = [int(255*self.sliderR.value),int(255*self.sliderG.value),int(255*self.sliderB.value)]
        self.window3D.model.colors = colvalRGB*STEPS

    def change_fov(self,is_pressed):
        self.window3D.set_fov(int(65 + self.sliderFOV.value*45))


if __name__ == '__main__':

    window3D = Window3D(line, width=400, height=300, caption='Model',resizable=True)
    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST)


    windowUI = WindowUI(window3D,width=700, height=400, caption='UI',resizable=True)


    pyglet.app.run()
