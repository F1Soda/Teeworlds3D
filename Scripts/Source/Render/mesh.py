import typing
import moderngl
import numpy as np


class Mesh:
    def __init__(self, ctx: moderngl.Context, name: str, data_format: str, attributes: typing.List):
        self.ctx = ctx
        self.name = name
        self.data_format = data_format
        self.attributes = attributes

        self.triangle_vertices = None
        self.vertices = None
        self.indices = None
        # self.indices = None
        self.normals = None
        self.tex_coord = None
        self.hidden_vertices = None
        # self.tex_coord_indices = None
        self._vbo = None
        self._hidden_vbo = None

    @property
    def vbo(self):
        if self._vbo is None:
            self._vbo = self.get_vbo()
        return self._vbo

    @property
    def hidden_vbo(self):
        if self._hidden_vbo is None:
            self._hidden_vbo = self.ctx.buffer(self.hidden_vertices)
        return self._hidden_vbo

    def reconstruct_vbo(self):
        self._vbo = self.get_vbo()
        return self._vbo

    def create_vertex_data(self) -> np.ndarray:
        vertex_data = self.triangle_vertices
        if self.tex_coord is not None:
            vertex_data = np.hstack([vertex_data, self.tex_coord])
        if self.normals is not None:
            vertex_data = np.hstack([vertex_data, self.normals])
        return vertex_data

    def get_vbo(self):
        vbo = self.ctx.buffer(self.create_vertex_data())
        return vbo

    def destroy(self):
        self.ctx = None
        self.vbo.release()
