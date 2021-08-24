import pyglet

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
line_coords = [0]*(STEPS*3)
for step in range(STEPS):
    stepoffset = step*3
    line_coords[stepoffset],line_coords[stepoffset+1],line_coords[stepoffset+2] = [coord*0.02 for coord in lorenz.get_location()]
    lorenz.step()

line = pyglet.graphics.vertex_list(STEPS, 'v3f/static', 'c3B/static')
line.vertices = line_coords
line.colors = [255]*3*STEPS
line.draw(pyglet.gl.GL_LINE_STRIP)


pyglet.app.run()
