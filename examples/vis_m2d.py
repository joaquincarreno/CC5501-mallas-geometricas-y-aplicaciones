import pyglet
from OpenGL import GL
import numpy as np
import os
from pathlib import Path

from sys import argv

from algorithms.load import read_m2d


def translate(tx, ty, tz):
    return np.array(
        [[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]], dtype=np.float32
    )


def uniformScale(s):
    return np.array(
        [[s, 0, 0, 0], [0, s, 0, 0], [0, 0, s, 0], [0, 0, 0, 1]], dtype=np.float32
    )


# A class to store the application control
class Controller:
    x = 0.0
    y = 0.0
    zoom = 1.0


controller = Controller()

path_to_this_file = Path(os.path.dirname(__file__))

try:
    m2d_file = argv[1]
except:
    print("file not specified")
    exit()

if __name__ == "__main__":
    width = 700
    height = 700
    win = pyglet.window.Window(width, height)

    vertices, indices = read_m2d(path_to_this_file / "../assets" / m2d_file)
    controller.zoom = 1 / max(vertices)

    with open(path_to_this_file / "../shaders/simple_vertex_program.glsl") as f:
        vertex_source_code = f.read()

    with open(path_to_this_file / "../shaders/dummy_fragment_program.glsl") as f:
        fragment_source_code = f.read()

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    gpu_data = pipeline.vertex_list_indexed(
        len(vertices) // 3, GL.GL_TRIANGLES, indices
    )
    gpu_data.position[:] = vertices
    gpu_data.color[:] = [1.0] * len(vertices)

    pipeline.use()

    @win.event
    def on_key_press(key, mod):
        if key == pyglet.window.key.UP:
            controller.y += 0.005
        elif key == pyglet.window.key.DOWN:
            controller.y += -0.005
        elif key == pyglet.window.key.LEFT:
            controller.x += -0.005
        elif key == pyglet.window.key.RIGHT:
            controller.x += 0.005

    @win.event
    def on_draw():
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        GL.glPointSize(5)

        win.clear()
        pipeline.use()

        pipeline["translate"] = translate(controller.x, controller.y, 0.0).reshape(
            16, 1, order="F"
        )
        pipeline["scale"] = uniformScale(controller.zoom).reshape(16, 1, order="F")

        gpu_data.draw(GL.GL_TRIANGLES)

    pyglet.app.run()
