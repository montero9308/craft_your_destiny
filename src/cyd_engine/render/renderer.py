from __future__ import annotations

from array import array
from dataclasses import dataclass
from typing import Any

from cyd_engine.render.shapes import Mesh

VERTEX_SHADER = """
#version 330
in vec3 in_position;

uniform mat4 u_mvp;

void main() {
    gl_Position = u_mvp * vec4(in_position, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330
uniform vec3 u_color;
out vec4 fragColor;

void main() {
    fragColor = vec4(u_color, 1.0);
}
"""


def _identity_mat4() -> tuple[float, ...]:
    return (
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    )


def flatten_mesh(mesh: Mesh) -> tuple[array[float], array[int]]:
    vertices = array("f")
    for x, y, z in mesh.vertices:
        vertices.extend((x, y, z))

    indices = array("I")
    for i0, i1, i2 in mesh.indices:
        indices.extend((i0, i1, i2))

    return vertices, indices


@dataclass(slots=True)
class ModernGLRenderer:
    """Renderer mínimo con ModernGL + shaders para terreno low-poly."""

    ctx: Any
    program: Any = None
    vao: Any = None
    vbo: Any = None
    ibo: Any = None

    def setup(self, mesh: Mesh) -> None:
        vertices, indices = flatten_mesh(mesh)
        self.program = self.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.ibo = self.ctx.buffer(indices.tobytes())
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, "3f", "in_position")], self.ibo)

    def render(self) -> None:
        if self.program is None or self.vao is None:
            return

        self.ctx.clear(0.07, 0.09, 0.12, 1.0)
        self.program["u_mvp"].write(array("f", _identity_mat4()).tobytes())
        self.program["u_color"].value = (0.37, 0.74, 0.42)
        self.vao.render()
