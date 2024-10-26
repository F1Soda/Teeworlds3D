import Scripts.Source.Components.Colliders.collider as collider_m
import Scripts.Source.Physic.physic_utils as physic_utils_m
import glm

NAME = 'Mesh Collider'
DESCRIPTION = 'Collider'


class MeshCollider(collider_m.Collider):
    def __init__(self, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self._mesh_filter = None
        self._center = None

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

    def find_furthest_point(self, direction) -> glm.vec3:
        max_point = glm.vec3()

        max_dot = -10e9
        #pos_cross_dir = glm.dot(self.transformation.pos, direction)
        for vertex in self.vertices:
            dot = glm.dot(vertex, direction)
            if dot > max_dot:
                max_dot = dot
                max_point = vertex

        return max_point + self.transformation.pos

    def get_collide_point(self, collider):
        simplex = physic_utils_m.gjk(self, collider)
        if simplex is None:
            return None
        return physic_utils_m.epa(simplex, self, collider)

    def init(self, app, rely_object):
        super().init(app, rely_object)