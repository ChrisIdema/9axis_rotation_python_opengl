# path = '../models/scifi_cartoon_rocket.obj'
path = '../models/10475_Rocket_Ship_v1_L3.obj'

import pyglet
import pywavefront
from pywavefront import visualization
from pyglet.gl import *
from pyglet.window import key
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import serial
import json

# from tinyQuaternion import Quaternion
# import numpy as np

ser = serial.Serial('COM4',115200,timeout=0)

window = pyglet.window.Window(resizable=True)
window.projection = pyglet.window.Projection3D(zfar=1000)
scene = pywavefront.Wavefront(path)

buffer = ''

def timer(self):

    global buffer
    # lines =  ser.readlines(-1)
    # print('lines:')
    # print(lines)
    # if 
    
    len = ser.in_waiting
    if len > 0:
        string = ser.read(len).decode("utf-8") 
        buffer += string
        last = buffer.rfind('\n')
        if last >= 0:
            second_last = buffer[0:last].rfind('\n')
            if second_last >= 0:
                last_line = buffer[second_last+1:last] # extract last line starting and ending with newline
                buffer = buffer[last:-1] # delete everything before last newline
                q = json.loads(last_line)
                # print(q)
                # q = Quaternion(q=np.array([q['quat_w'],q['quat_w'],q['quat_w'],q['quat_w']]))
                # print(q)




@window.event
def on_draw():
    # print('draw')
    window.clear()
    visualization.draw(scene)

@window.event
def on_key_press(symbol, modifiers):

    # glTranslated(0, 0, 200)   

    if symbol == key.G:
        glRotated(22,0,1,0)
        # glTranslated(25, 0, 0)
    if symbol == key.B:
        glRotated(-22,0,1,0)
        # glTranslated(-25, 0, 0)
    if symbol == key.H:
        glRotated(22,1,0,0)
        # glTranslated(0, 25, 0)     
    if symbol == key.N:
        glRotated(-22,1,0,0)
        # glTranslated(0, -25, 0)   
    if symbol == key.J:
        glRotated(22,0,0,1)
        # glTranslated(0, 25, 0)     
    if symbol == key.M:
        glRotated(-22,0,0,1)
        # glTranslated(0, -25, 0)   
    if symbol == key.Q:
        glPopMatrix()
        glPushMatrix();
        glTranslated(0, 0, 200)   
        glRotated(-22,0,1,0)
        glTranslated(0, 0, -200)

    # glTranslated(0, 0, -200)

if __name__ == "__main__":
    # Setando estados para visualização da câmera
    glViewport(0, 0, 500,500)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)

    # Changing the starting position of the center
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

    glTranslated(0, 0, 100)



    for _ in range(4):
        glRotated(25,0,1,0)
        glTranslated(35, 0, 0)

    glRotated(100,0,1,0)
    glTranslated(0, 0, 200)
    glRotated(-100,1,0,0)
    glTranslated(-100, -275, -250)  

    glScale(0.75, 0.75, 0.75)

    glClearColor(0.85, 0.85, 0.85, 1);



    # a = (GLfloat * 16)()
    # mvm = glGetFloatv(GL_MODELVIEW_MATRIX, a)
    # print(list(a))
 
    pyglet.clock.schedule_interval(timer, 1/10);

    pyglet.app.run()