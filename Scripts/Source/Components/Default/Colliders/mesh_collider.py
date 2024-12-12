import Scripts.Source.Components.Default.Colliders.collider as collider_m
import Scripts.Source.Physic.physic_utils as physic_utils_m
import glm

NAME = 'Mesh Collider'
DESCRIPTION = 'Collider'


class MeshCollider(collider_m.Collider):
    def __init__(self, enable=True):

        super().__init__(NAME, DESCRIPTION, enable)
        self._mesh_filter = None
        self.base_name = "Collider"
        self._center = None

    @property
    def max_radius_of_collisions(self):
        if self._max_radius_of_collisions is None:
            self._max_radius_of_collisions = 0
            for vertex in self.mesh_filter.mesh.vertices:
                self._max_radius_of_collisions = max(self._max_radius_of_collisions,
                                                     glm.length(glm.mul(self.m_model, vertex) - self.center))
        return self._max_radius_of_collisions

    @property
    def m_model(self):
        return self.transformation.m_model

    @property
    def center(self):
        if self.mesh_filter is None:
            return None
        if self._center is None:
            self._center = glm.vec3()
            n = 0
            for vertex in self.mesh_filter.mesh.vertices:
                self._center += vertex
                n += 1
            self._center /= n

        return self._center

    @property
    def mesh_filter(self):
        if self._mesh_filter is None:
            self._mesh_filter = self.rely_object.get_component_by_name("Mesh Filter")
        return self._mesh_filter

    @mesh_filter.setter
    def mesh_filter(self, value):
        self._mesh_filter = value

    @property
    def hidden_vbo(self):
        if self.mesh_filter is None:
            return None
        return self.mesh_filter.mesh.hidden_vbo

    @property
    def vertices(self):
        if self.mesh_filter is None:
            return None
        return self.mesh_filter.vertices

    def get_collide_point(self, collider):
        simplex = physic_utils_m.gjk(self, collider)
        if simplex is None:
            return None
        return physic_utils_m.epa(simplex, self, collider)
