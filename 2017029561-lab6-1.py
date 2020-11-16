import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
gCamAng = 0.
gCamHeight = 1.
glVertexArray = None
glIndexArray = None

def createVertexAndIndexArrayIndexed():
   varr = np.array([
      [.0, .0, .0],
      [1.5, .0, .0],
      [.0, 1.5, .0],
      [.0, .0, 1.5],
   ], 'float32')
   iarr = np.array([
      [0, 1, 2],
      [0, 2, 3],
      [0, 1, 3],
   ])
   return varr, iarr

def drawCube_glDrawElements():
   global glVertexArray, glIndexArray
   varr = glVertexArray
   iarr = glIndexArray
   glEnableClientState(GL_VERTEX_ARRAY)
   glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
   glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
   glBegin(GL_LINES)
   glColor3ub(255, 0, 0)
   glVertex3fv(np.array([0.,0.,0.]))
   glVertex3fv(np.array([1.,0.,0.]))
   glColor3ub(0, 255, 0)
   glVertex3fv(np.array([0.,0.,0.]))
   glVertex3fv(np.array([0.,1.,0.]))
   glColor3ub(0, 0, 255)
   glVertex3fv(np.array([0.,0.,0]))
   glVertex3fv(np.array([0.,0.,1.]))
   glEnd()

def render():
   global gCamAng, gCamHeight
   glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
   glEnable(GL_DEPTH_TEST)
   glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

   glLoadIdentity()
   gluPerspective(45, 1, 1,10)
   gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)
   
   drawFrame() 
   glColor3ub(255, 255, 255)
   drawCube_glDrawElements()

def key_callback(window, key, scancode, action, mods):
   global gCamAng, gCamHeight
   if action==glfw.PRESS or action==glfw.REPEAT:
      if key==glfw.KEY_1:
         gCamAng += np.radians(-10)
      elif key==glfw.KEY_3:
         gCamAng += np.radians(10)
      elif key==glfw.KEY_2:
         gCamHeight += .1
      elif key==glfw.KEY_W:
         gCamHeight += -.1

def windows_callback(window, width, height):
   glViewport(0, 0, width, height)

def main():
   global glVertexArray, glIndexArray, gCamAng, gCamHeight
   gCamAng = np.radians(30)
   gCamHeight = 1
   if not glfw.init():
      return
   window = glfw.create_window(480,480,'2017029561', None,None)
   if not window:
      glfw.terminate()
      return
   glfw.make_context_current(window)
   glfw.set_key_callback(window, key_callback)
   glfw.set_framebuffer_size_callback(window, windows_callback)

   glVertexArray, glIndexArray = createVertexAndIndexArrayIndexed()
   while not glfw.window_should_close(window):
      glfw.poll_events()
      render()
      glfw.swap_buffers(window)
   
   glfw.terminate()

if __name__ == "__main__":
   main()
