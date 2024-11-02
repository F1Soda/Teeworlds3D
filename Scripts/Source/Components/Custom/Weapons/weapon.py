import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m

NAME = 'Weapon'
DESCRIPTION = 'Abstract Weapon'


class Weapon(component_m.Component):
    def __init__(self, damage, magazine_size, reload_time, fire_speed, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        self.damage = damage
        self.magazine_size = magazine_size
        self.reload_time = reload_time
        self.fire_speed = fire_speed

        self._transformation = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)

    def fire(self):
        ...

    def reload(self):
        ...

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
        ...
