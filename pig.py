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

from squaternion import Quaternion
import numpy as np

ser = serial.Serial('COM4',115200,timeout=0)

window = pyglet.window.Window(resizable=True)
window.projection = pyglet.window.Projection3D(zfar=1000)
scene = pywavefront.Wavefront(path)

buffer = ''

init_yaw = None

def timer(self):

    global buffer
    
    len = ser.in_waiting
    if len > 0:
        string = ser.read(len).decode("utf-8")
        buffer_old = str(buffer)
        buffer += string
        last = buffer.rfind('\n')
        if last >= 0:
            second_last = buffer[0:last].rfind('\n')
            if second_last >= 0:
                last_line = buffer[second_last+1:last] # extract last line starting and ending with newline
                
                try:
                    q = json.loads(last_line)
                    q = Quaternion(q['quat_w'],q['quat_x'],q['quat_y'],q['quat_z'])
                    buffer = buffer[last:] # delete everything before last newline
                except:
                    print('invalid input')
                    print('buffer:',buffer)
                    buffer = ''
                    return               
                
                # delete current matrix and replace with copy of initialized matrix:
                glPopMatrix()
                glPushMatrix()

                e = q.to_euler(degrees=True)

                global init_yaw
                if init_yaw == None:
                    init_yaw = e[2]
                    print(q)
                    print(init_yaw)

                glTranslated(0, 0, 200)   

                q_yaw = Quaternion.from_euler(0,0,init_yaw,degrees=True)

                q = q_yaw*q

                #flip model around x axis, because sensor is upside down:
                q_flip = Quaternion.from_angle_axis(180, [1,0,0],degrees=True)
                q = q*q_flip

                r = np.array(q.to_rot())

                r4x4 = np.array([[r[0,0],r[1,0],r[2,0],0],
                                 [r[0,1],r[1,1],r[2,1],0],
                                 [r[0,2],r[1,2],r[2,2],0],
                                 [0,0,0,1]])
                
                glMultMatrixd(r4x4)

                glTranslated(0, 0, -200)


@window.event
def on_draw():
    window.clear()
    visualization.draw(scene)

if __name__ == "__main__":
    glViewport(0, 0, 500,500)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)

    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(0.85, 0.85, 0.85, 1);

    array = np.array([[0,0,1,0],
                      [1,0,0,0],
                      [0,1,0,0],
                      [0,-150,-600,1]])

    glLoadMatrixd(array)

    glPushMatrix();
 
    pyglet.clock.schedule_interval(timer, 1/60);

    pyglet.app.run()
