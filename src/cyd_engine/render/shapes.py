from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin


@dataclass(slots=True)
class Mesh:
    vertices: list[tuple[float, float, float]]
    indices: list[tuple[int, int, int]]

    @property
    def triangle_count(self) -> int:
        return len(self.indices)


class PrimitiveBuilder:
    """Genera mallas low-poly sin modelos externos."""

    def cube(self, size: float = 1.0) -> Mesh:
        h = size / 2.0
        vertices = [
            (-h, -h, -h),
            (h, -h, -h),
            (h, h, -h),
            (-h, h, -h),
            (-h, -h, h),
            (h, -h, h),
            (h, h, h),
            (-h, h, h),
        ]
        indices = [
            (0, 1, 2), (0, 2, 3),
            (4, 5, 6), (4, 6, 7),
            (0, 1, 5), (0, 5, 4),
            (2, 3, 7), (2, 7, 6),
            (1, 2, 6), (1, 6, 5),
            (0, 3, 7), (0, 7, 4),
        ]
        return Mesh(vertices, indices)

    def cylinder(self, radius: float = 0.5, height: float = 1.0, segments: int = 8) -> Mesh:
        vertices: list[tuple[float, float, float]] = []
        indices: list[tuple[int, int, int]] = []
        for i in range(segments):
            a = 2 * pi * i / segments
            x, z = radius * cos(a), radius * sin(a)
            vertices.append((x, -height / 2, z))
            vertices.append((x, height / 2, z))

        for i in range(0, segments * 2, 2):
            n = (i + 2) % (segments * 2)
            indices.append((i, n, i + 1))
            indices.append((i + 1, n, n + 1))
        return Mesh(vertices, indices)


class MeshFactory:
    def from_heightmap(self, heightmap: list[list[float]]) -> Mesh:
        vertices: list[tuple[float, float, float]] = []
        indices: list[tuple[int, int, int]] = []
        width = len(heightmap[0]) if heightmap else 0

        for z, row in enumerate(heightmap):
            for x, h in enumerate(row):
                vertices.append((float(x), h, float(z)))

        for z in range(len(heightmap) - 1):
            for x in range(width - 1):
                i = z * width + x
                indices.append((i, i + width, i + 1))
                indices.append((i + 1, i + width, i + width + 1))

        return Mesh(vertices, indices)
