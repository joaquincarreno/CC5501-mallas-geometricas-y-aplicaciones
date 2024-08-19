import pyglet
from OpenGL import GL
import numpy as np
import os
from pathlib import Path

from algorithms.ray_casting import *


# A class to store the application control
class Controller:
    x = 0.0
    y = 0.0


controller = Controller()


if __name__ == "__main__":
    width = 700
    height = 700
    win = pyglet.window.Window(width, height)

    # Define the vertices of the polygon
    vertices = np.array(
        [
            -0.5,
            -0.5,
            0.0,  # Vértice 0
            0.5,
            -0.5,
            0.0,  # Vértice 1
            0.7,
            0.5,
            0.0,  # Vértice 2
            0.0,
            0.7,
            0.0,  # Vértice 3
            -0.7,
            0.5,
            0.0,  # Vértice 4
        ],
        dtype=np.float32,
    )

    # Define the indices of the polygon (for GL_POLYGON it is not necessary)
    indices = np.array([0, 1, 2, 3, 4], dtype=np.uint32)
    with open(
        Path(os.path.dirname(__file__)) / "../shaders/dummy_vertex_program.glsl"
    ) as f:
        vertex_source_code = f.read()

    with open(
        Path(os.path.dirname(__file__)) / "../shaders/dummy_fragment_program.glsl"
    ) as f:
        fragment_source_code = f.read()

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    gpu_data = pipeline.vertex_list_indexed(len(vertices) // 3, GL.GL_POLYGON, indices)
    gpu_data.position[:] = vertices
    gpu_data.color[:] = [1.0] * len(vertices)

    dot = pipeline.vertex_list_indexed(1, GL.GL_POINT, [0])
    dot.position[:] = [controller.x, controller.y, 0]
    dot.color[:] = [1, 0, 0]

    pipeline.use()

    @win.event
    def on_key_press(key, mod):
        if key == pyglet.window.key.UP:
            controller.y += 0.05
        elif key == pyglet.window.key.DOWN:
            controller.y -= 0.05
        elif key == pyglet.window.key.LEFT:
            controller.x -= 0.05
        elif key == pyglet.window.key.RIGHT:
            controller.x += 0.05
        elif key == pyglet.window.key.SPACE:
            point = (controller.x, controller.y)
            polygon = [
                (vertices[i], vertices[i + 1]) for i in range(0, len(vertices), 3)
            ]
            inside, crossing = ray_casting(point, polygon)
            print(f"Esta dentro: {inside}, número de intersecciones: {crossing}")

    @win.event
    def on_draw():
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        GL.glPointSize(5)

        win.clear()
        pipeline.use()
        gpu_data.draw(GL.GL_LINE_LOOP)

        dot.position[:] = [controller.x, controller.y, 0]
        dot.draw(GL.GL_POINTS)

    pyglet.app.run()
