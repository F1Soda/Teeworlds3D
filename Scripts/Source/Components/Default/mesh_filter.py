import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m

NAME = 'Mesh Filter'
DESCRIPTION = 'Component for work with the Mesh data'


class MeshFilter(component_m.Component):
    def __init__(self, mesh, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self.mesh = mesh
        self._transformation = None
        self._vertices = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)

    @property
    def vertices(self):
        if self.mesh is None:
            raise Exception("ERROR: mesh in mesh filter is None!")
        return self.mesh.vertices

    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def delete(self):
        self._transformation = None
        self.mesh = None
        self.rely_object = None

    def serialize(self) -> {}:
        return {
            'mesh': self.mesh.name,
            'enable': self.enable
        }
