import pyglet
from pyglet.gl import *
import noise
import numpy as np
from pyglet.window import key, mouse

window = pyglet.window.Window(width=1000, height=1000, resizable=True)

w = 24
minHeight = 1
maxHeight = 150
noiseScale = 0.005
timeScale = 0.0002
speed = 3

camX, camY, camZ = 0, 0, 500
camRotX, camRotY = 0, 0
time = 0

def generate_height_map(width, height, scale):
    return np.array([[noise.pnoise3(x * scale, 0, y * scale) for x in range(width)] for y in range(height)])

height_map = generate_height_map(100, 100, noiseScale)

def draw_box(x, y, z, size, color):
    glColor3f(*color)
    glPushMatrix()
    glTranslatef(x, y, z)
    glBegin(GL_QUADS)
    for dx, dy, dz in [(0, 0, 0), (size, 0, 0), (size, size, 0), (0, size, 0),
                       (0, 0, size), (size, 0, size), (size, size, size), (0, size, size)]:
        glVertex3f(dx, dy, dz)
    glEnd()
    glPopMatrix()

@window.event
def on_draw():
    global camX, camY, camZ, camRotX, camRotY, time
    window.clear()
    glLoadIdentity()

    glRotatef(camRotX, 1, 0, 0)
    glRotatef(camRotY, 0, 1, 0)
    glTranslatef(-camX, -camY, -camZ)

    for z in range(len(height_map)):
        for x in range(len(height_map[z])):
            noise_value = height_map[z][x]
            h = np.interp(noise_value, [-1, 1], [minHeight, maxHeight])
            color_value = np.interp(noise_value, [-1, 1], [0, 1])

            if color_value <= 0.5:
                colorname = (0, 0.4, 0.57)
            elif 0.5 < color_value < 0.65:
                colorname = (0.94, 0.86, 0.89)
            else:
                colorname = (0.11, 0.56, 0.4)

            draw_box(x * w - len(height_map[z]) * w / 2, h / 2, z * w - len(height_map) * w / 2, w, colorname)

@window.event
def on_key_press(symbol, modifiers):
    global camX, camY, camZ, camRotX, camRotY, time
    if symbol == key.W:
        camX += speed * np.sin(np.radians(camRotY))
        camZ -= speed * np.cos(np.radians(camRotY))
    if symbol == key.S:
        camX -= speed * np.sin(np.radians(camRotY))
        camZ += speed * np.cos(np.radians(camRotY))
    if symbol == key.A:
        camX -= speed * np.cos(np.radians(camRotY))
        camZ -= speed * np.sin(np.radians(camRotY))
    if symbol == key.D:
        camX += speed * np.cos(np.radians(camRotY))
        camZ += speed * np.sin(np.radians(camRotY))
    if symbol == key.E:
        camY += speed
    if symbol == key.Q:
        camY -= speed
    if symbol == key.F:
        time += 100
    if symbol == key.G:
        time -= 100

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global camRotX, camRotY
    if buttons & mouse.LEFT:
        camRotY += dx * 0.1
        camRotX -= dy * 0.1

pyglet.app.run()
