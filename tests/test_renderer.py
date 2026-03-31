from cyd_engine.render.renderer import _identity_mat4, flatten_mesh
from cyd_engine.render.shapes import Mesh


def test_identity_matrix_has_16_values() -> None:
    mat = _identity_mat4()
    assert len(mat) == 16
    assert mat[0] == 1.0
    assert mat[5] == 1.0
    assert mat[10] == 1.0
    assert mat[15] == 1.0


def test_flatten_mesh_packs_vertices_and_indices() -> None:
    mesh = Mesh(vertices=[(0.0, 1.0, 2.0), (3.0, 4.0, 5.0), (6.0, 7.0, 8.0)], indices=[(0, 1, 2)])
    vertices, indices = flatten_mesh(mesh)
    assert list(vertices) == [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    assert list(indices) == [0, 1, 2]
