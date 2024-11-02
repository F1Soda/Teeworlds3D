import Scripts.Source.Components.Default.Colliders.collider as collider_m
import Scripts.Source.Physic.physic_utils as physic_utils_m
import Scripts.Source.Render.library as library_m

import glm

NAME = 'Box Collider'
DESCRIPTION = 'Collider'


class BoxCollider(collider_m.Collider):
    def __init__(self, enable=True):
        self._size = glm.vec3(1)
        self.offset = glm.vec3(0)
        super().__init__(NAME, DESCRIPTION, enable)
        self.use_transform_model_matrix = True
        self.base_name = "Collider"

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self.try_precalculate_collider()

    @property
    def m_model(self):
        if self.use_transform_model_matrix:
            return self.transformation.m_model

        self._m_model = glm.translate(self.transformation.m_t, self.offset)
        self._m_model = glm.scale(self._m_model, self._size)
        return self._m_model

    @property
    def size(self):
        if self.use_transform_model_matrix:
            return self.transformation.scale
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def try_precalculate_collider(self):
        mesh_filter = self.rely_object.get_component_by_name("Mesh Filter")
        if mesh_filter is None:
            return

    @property
    def vertices(self):
        if self._vertices is None:
            self._vertices = library_m.meshes['cube'].vertices
        return self._vertices

    @property
    def hidden_vbo(self):
        if self._hidden_vbo is None:
            self._hidden_vbo = self.app.ctx.buffer(library_m.meshes['cube'].hidden_vertices)
        return self._hidden_vbo

    def get_collide_point(self, collider):
        simplex = physic_utils_m.gjk(self, collider)
        if simplex is None:
            return None
        return physic_utils_m.epa(simplex, self, collider)
