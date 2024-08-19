import glfw
from OpenGL.GL import *
import numpy as np
import ctypes
from algorithms.ray_casting import *

# A class to store the application control
class Controller:
    x = 0.0
    y = 0.0

# we will use the global controller as communication with the callback function
controller = Controller()

# Keyboard callback function

def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return
    global controller
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            controller.y += 0.05
        elif key == glfw.KEY_DOWN:
            controller.y -= 0.05
        elif key == glfw.KEY_LEFT:
            controller.x -= 0.05
        elif key == glfw.KEY_RIGHT:
            controller.x += 0.05
        elif key == glfw.KEY_SPACE:
            point = (controller.x, controller.y)
            polygon = [(vertices[i], vertices[i+1]) for i in range(0, len(vertices), 3)]
            inside, crossing = ray_casting(point, polygon)
            print(f"Esta dentro: {inside}, número de intersecciones: {crossing}")


if __name__ == "__main__":
    # Initialize GLFW
    if not glfw.init():
        raise Exception("GLFW cannot be initialized!")

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(600, 600, "Ray Casting Example", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window cannot be created!")


    # Make the window's context current
    glfw.make_context_current(window)

    # Set the viewport
    glViewport(0, 0, 600, 600)

    # Define the vertices of the polygon
    vertices = np.array([
        -0.5, -0.5, 0.0,  # Vértice 0
        0.5, -0.5, 0.0,  # Vértice 1
        0.7, 0.5, 0.0,  # Vértice 2
        0.0, 0.7, 0.0,  # Vértice 3
        -0.7, 0.5, 0.0  # Vértice 4
    ], dtype=np.float32)


    # Define the indices of the polygon (for GL_POLYGON it is not necessary)
    indices = np.array([
        0, 1, 2, 3, 4
    ], dtype=np.uint32)

    # Create and bind the Vertex Array Object
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    # Create and bind the Vertex Buffer Object
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Create and bind the Element Buffer Object (optional for GL_POLYGON)
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Define the position attribute
    position = 0  # Assuming position is at location 0 in the shader
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    # Unbind the VAO
    glBindVertexArray(0)

    # Initialize point position
    point_pos = np.array([controller.x, controller.y], dtype=np.float32)

    # Set the keyboard callback
    glfw.set_key_callback(window, on_key)

    # Main loop
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        # Clear the color buffer
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw the polygon
        glColor3f(1.0, 1.0, 1.0)  # Green color
        glBindVertexArray(vao)
        glDrawArrays(GL_POLYGON, 0, len(vertices) // 3)
        glBindVertexArray(0)

        # Draw the moving point
        glColor3f(1.0, 0.0, 0.0)  # Red color
        glPointSize(10)  # Make the point larger
        glBegin(GL_POINTS)
        glVertex2f(controller.x, controller.y)
        glEnd()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    # Cleanup
    glDeleteBuffers(1, [vbo])
    glDeleteBuffers(1, [ebo])
    glDeleteVertexArrays(1, [vao])

    # Terminate GLFW
    glfw.terminate()

