import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.transformation as transformation_m
import glm

NAME = 'Light'
DESCRIPTION = 'Источник света'


class Light(component_m.Component):
    def __init__(self, color=(1, 1, 1), enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self.color = glm.vec3(color)

        self.intensity_ambient = 0.1 * self.color
        self.intensity_diffuse = 0.8 * self.color
        self.intensity_specular = 1.0 * self.color

        self._transformation = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)

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
        self.rely_object = None

    def serialize(self) -> {}:
        return {
            "color": ("vec", self.color.to_tuple()),
            'enable': self.enable
        }
