import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

gCamAng = np.radians(40)
gCamHeight = 2.5
lightColor = (1.,1.,1.,1.)
objectColor = (1.,0.,0.,1.)

def drawCube_glVertex():
   glBegin(GL_TRIANGLES)

   glNormal3f(0,0,1)# v0, v1, ... v5 normal
   glVertex3f(-1,1,1)# v0 position
   glVertex3f(1,-1,1)# v1 position
   glVertex3f(1,1,1)# v2 position

   glVertex3f(-1,1,1)# v3 position
   glVertex3f(-1,1,1)# v4 position
   glVertex3f(1,-1,1)# v5 position

   glNormal3f(0,0,-1)# v6, v7, ... v11 normal
   glVertex3f(-1,1,1)# v6 position
   glVertex3f(-1,-1,1)# v7 position
   glVertex3f(1,-1,-1)# v8 position

   glVertex3f(-1,1,1)# v9 position
   glVertex3f(1,-1,-1)# v10 position
   glVertex3f(-1,-1,-1)# v11 position

   glNormal3f(0,1,0)
   glVertex3f(-1,1,1)
   glVertex3f(1,1,1)
   glVertex3f(1,1,-1)

   glVertex3f(-1,1,1)
   glVertex3f(1,1,-1)
   glVertex3f(-1,1,-1)

   glNormal3f(0,-1,0)
   glVertex3f(-1,-1,1)
   glVertex3f(1,-1,-1)
   glVertex3f(1,-1,1)

   glVertex3f(-1,-1,1)
   glVertex3f(-1,-1,-1)
   glVertex3f(1,-1,-1)

   glNormal3f(1,0,0)
   glVertex3f(1,1,1)
   glVertex3f(1,-1,1)
   glVertex3f(1,-1,-1)

   glVertex3f(1,1,1)
   glVertex3f(1,-1,-1)
   glVertex3f(1,1,-1)

   glNormal3f(-1,0,0)
   glVertex3f(-1,1,1)
   glVertex3f(-1,-1,-1)
   glVertex3f(-1,-1,1)

   glVertex3f(-1,1,1)
   glVertex3f(-1,1,-1)
   glVertex3f(-1,-1,-1)

   glEnd()


def createVertexArraySeparate():
    varr = np.array([
        (0,0,1), # v0 normal
        ( -1 , 1 , 1 ), # v0 position
        (0,0,1), # v2 normal
        ( 1 , -1 , 1 ), # v2 position
        (0,0,1), # v1 normal
        ( 1 , 1 , 1 ), # v1 position
        (0,0,1), # v0 normal
        ( -1 , 1 , 1 ), # v0 position
        (0,0,1), # v3 normal
        ( -1 , -1 , 1 ), # v3 position
        (0,0,1), # v2 normal
        ( 1 , -1 , 1 ), # v2 position
        (0,0,-1),
        ( -1 , 1 , -1 ), # v4
        (0,0,-1),
        ( 1 , 1 , -1 ), # v5
        (0,0,-1),
        ( 1 , -1 , -1 ), # v6
        (0,0,-1),
        ( -1 , 1 , -1 ), # v4
        (0,0,-1),
        ( 1 , -1 , -1 ), # v6
        (0,0,-1),
        ( -1 , -1 , -1 ), # v7
        (0,1,0),
        ( -1 , 1 , 1 ), # v0
        (0,1,0),
        ( 1 , 1 , 1 ), # v1
        (0,1,0),
        ( 1 , 1 , -1 ), # v5
        (0,1,0),
        ( -1 , 1 , 1 ), # v0
        (0,1,0),
        ( 1 , 1 , -1 ), # v5
        (0,1,0),
        ( -1 , 1 , -1 ), # v4
        (0,-1,0),
        ( -1 , -1 , 1 ), # v3
        (0,-1,0),
        ( 1 , -1 , -1 ), # v6
        (0,-1,0),
        ( 1 , -1 , 1 ), # v2

        (0,-1,0),
        ( -1 , -1 , 1 ), # v3
        (0,-1,0),
        ( -1 , -1 , -1 ), # v7
        (0,-1,0),
        ( 1 , -1 , -1 ), # v6
        (1,0,0),
        ( 1 , 1 , 1 ), # v1
        (1,0,0),
        ( 1 , -1 , 1 ), # v2
        (1,0,0),
        ( 1 , -1 , -1 ), # v6
        (1,0,0),
        ( 1 , 1 , 1 ), # v1
        (1,0,0),
        ( 1 , -1 , -1 ), # v6
        (1,0,0),
        ( 1 , 1 , -1 ), # v5
        (-1,0,0),
        ( -1 , 1 , 1 ), # v0
        (-1,0,0),
        ( -1 , -1 , -1 ), # v7
        (-1,0,0),
        ( -1 , -1 , 1 ), # v3
        (-1,0,0),
        ( -1 , 1 , 1 ), # v0
        (-1,0,0),
        ( -1 , 1 , -1 ), # v4
        (-1,0,0),
        ( -1 , -1 , -1 ), # v7
        ], 'float32')
    return varr

def l2norm(v):
   return np.sqrt(np.dot(v, v))

def normalized(v):
   return 1/l2norm(v) * np.array(v)

gVertexArrayIndexed = None
gIndexArray = None

def drawCube_glDrawElements():
   global gVertexArrayIndexed, gIndexArray
   varr = gVertexArrayIndexed
   iarr = gIndexArray
   glEnableClientState(GL_VERTEX_ARRAY)
   glEnableClientState(GL_NORMAL_ARRAY)
   glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
   glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
   glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def render(ang):
   global gCamAng,gCamHeight
   glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

   glEnable(GL_DEPTH_TEST)

   glMatrixMode(GL_PROJECTION) 
   # use projection matrix stack for projection transformation for correct lighting
   glLoadIdentity()
   gluPerspective(45,1,1,10)

   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()
   
   gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng),0,0,0,0,1,0)
   
   drawFrame()
   
   glEnable(GL_LIGHTING)# try to uncomment: no lighting
   glEnable(GL_LIGHT0)
   
   # light position
   glPushMatrix()

   # glRotatef(ang,0,1,0)  # try to uncomment: rotate light
   lightPos=(3.,4.,5.,1.)#
   glLightfv(GL_LIGHT0,GL_POSITION,lightPos)
   
   glPopMatrix()
   # light intensity for each color channel
   ambientLightColor=(.1,.1,.1,1.)
   diffuseLightColor=(1.,1.,1.,1.)
   specularLightColor=(1.,1.,1.,1.)
   glLightfv(GL_LIGHT0,GL_AMBIENT,ambientLightColor)
   glLightfv(GL_LIGHT0,GL_DIFFUSE,diffuseLightColor)
   glLightfv(GL_LIGHT0,GL_SPECULAR,specularLightColor)
   
   # material reflectance for each color channel
   diffuseObjectColor =(1.,0.,0.,1.)
   specularObjectColor =(1.,0.,0.,1.)
   glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,diffuseObjectColor)
   
   glPushMatrix()

   glColor3ub(0,0,255)
   
   drawCube_glDrawElements()
   glPopMatrix()
   
   glDisable(GL_LIGHTING)

def modifiedIndexes(): 
   varr = np.array([
      normalized([ 1, 1,-1]),
      [ 1, 1,-1],
      normalized([-1, 1,-1]),
      [-1, 1,-1],
      normalized([-1, 1, 1]),
      [-1, 1, 1],
      normalized([ 1, 1, 1]),
      [ 1, 1, 1],
      normalized([ 1,-1, 1]),
      [ 1,-1, 1],
      normalized([-1,-1, 1]),
      [-1,-1, 1],
      normalized([-1,-1,-1]),
      [-1,-1,-1],
      normalized([ 1,-1,-1]),
      [ 1,-1,-1],
   ], 'float32')
   iarr = np.array([
      [0,1,2],
      [0,2,3],
      [4,5,6],
      [4,6,7],
      [3,2,5],
      [3,5,4],
      [7,6,1],
      [7,1,0],
      [2,1,6],
      [2,6,5],
      [0,3,4],
      [0,4,7],
   ])
   return varr, iarr

def drawFrame():
   glBegin(GL_LINES)
   glColor3ub(255,0,0)
   glVertex3fv(np.array([0.,0.,0.]))
   glVertex3fv(np.array([1.,0.,0.]))
   glColor3ub(0,255,0)
   glVertex3fv(np.array([0.,0.,0.]))
   glVertex3fv(np.array([0.,1.,0.]))
   glColor3ub(0,0,255)
   glVertex3fv(np.array([0.,0.,0]))
   glVertex3fv(np.array([0.,0.,1.]))
   glEnd()

def key_callback(window,key,scancode,action,mods):
   global gCamAng,gCamHeight,lightColor,objectColor
   if action == glfw.PRESS or action==glfw.REPEAT:
      if key == glfw.KEY_1:
         gCamAng += np.radians(-10)
      elif key == glfw.KEY_3:
         gCamAng += np.radians(10)
      elif key == glfw.KEY_2:
         gCamHeight += .1
      elif key == glfw.KEY_W:
         gCamHeight += -.1
      elif key == glfw.KEY_A:
         lightColor = (1.,0.,0.,1.)
      elif key == glfw.KEY_S:
         lightColor = (0.,1.,0.,1.)
      elif key == glfw.KEY_D:
         lightColor = (0.,0.,1.,1.)
      elif key == glfw.KEY_F:
         lightColor = (1.,1.,1.,1.)
      elif key == glfw.KEY_Z:
         objectColor = (1.,0.,0.,1.)
      elif key == glfw.KEY_X:
         objectColor = (0.,1.,0.,1.)
      elif key == glfw.KEY_C:
         objectColor = (0.,0.,1.,1.)
      elif key == glfw.KEY_V:
         objectColor = (1.,1.,1.,1.)



gVertexArraySeparate = None

def main():
   global gVertexArraySeparate
   global gVertexArrayIndexed, gIndexArray
   if not glfw.init(): return
   window = glfw.create_window(480,480,'2017029561', None,None)
   if not window:
      glfw.terminate()
      return
   glfw.make_context_current(window)
   glfw.set_key_callback(window, key_callback)
   glfw.swap_interval(1)

   gVertexArraySeparate = createVertexArraySeparate()
   gVertexArrayIndexed, gIndexArray = modifiedIndexes()

   count = 0
   while not glfw.window_should_close(window):
      glfw.poll_events()
      ang = count % 360
      render(ang)
      count += 1
      glfw.swap_buffers(window)
   glfw.terminate()

if __name__ =="__main__":
   main()
