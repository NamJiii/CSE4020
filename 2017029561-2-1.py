import glfw
from OpenGL.GL import *
import numpy as np

modes = GL_LINE_LOOP

def kb_hit(window, key, scancode, action, mods):
    global modes
    if action == glfw.PRESS:
        input = key - 48
        if input >= 0 and input <= 9:
            modes = {   
                1: GL_POINTS,
                2: GL_LINES,
                3: GL_LINE_STRIP,
                4: GL_LINE_LOOP,
                5: GL_TRIANGLES,
                6: GL_TRIANGLE_STRIP,
                7: GL_TRIANGLE_FAN,
                8: GL_QUADS,
                9: GL_QUAD_STRIP,
                0: GL_POLYGON,
            }[input]

def render():
    global modes

    side = 12
    step = 2 * np.pi / side
    start = np.pi/2
    end = -3*np.pi/2
    
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(modes)
    glColor3ub(255, 255, 255)

    for rad in np.arange(start, end, -step):
        glVertex2fv((np.sin(rad), np.cos(rad)))
    glEnd()

def main():
    global modes
    if not glfw.init(): return
    window = glfw.create_window(480, 480, "2017029561-2-1", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, kb_hit)
    glfw.make_context_current(window)

    modes = GL_LINE_LOOP
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
