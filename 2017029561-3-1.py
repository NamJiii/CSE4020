import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

T = np.array([[1., 0., 0.],
              [0., 1., 0.],
              [0., 0., 1.]])
def kb_hit(window, key, scancode, action, mods):
    global T, N;
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == 81:
            T = np.array([[1., 0., -.1],
                          [0., 1., 0.],
                          [0., 0., 1.]]) @ T
        elif key == 69:
            T = np.array([[1., 0., .1],
                          [0., 1., 0.],
                          [0., 0., 1.]]) @ T
        elif key == 65:
            T = T @ np.array([[np.cos(np.radians(10)), -np.sin(np.radians(10)),0.],
                              [np.sin(np.radians(10)), np.cos(np.radians(10)),0.],
                              [0., 0., 1.]])
        elif key == 68:
            T = T @ np.array([[np.cos(np.radians(-10)), -np.sin(np.radians(-10)),0.],
                              [np.sin(np.radians(-10)), np.cos(np.radians(-10)),0.],
                              [0., 0., 1.]])
        elif key == 49:
            T = np.array([[1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., 1.]])

        elif key == 87:
            T = np.array([[.9, 0., 0.],
                          [0., 1., 0.],
                          [0., 0., 1.]]) @ T            

        elif key == 83:
            
            T = np.array([[np.cos(np.radians(10)), -np.sin(np.radians(10)),0.],
                              [np.sin(np.radians(10)), np.cos(np.radians(10)),0.],
                              [0., 0., 1.]]) @ T
def render(T):

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
  
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()


    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()

def main():
    global T
    
    if not glfw.init():
        return
    window = glfw.create_window(480,480, "2017029561-3-1", None,None)

    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, kb_hit)
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(T)
        
        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
