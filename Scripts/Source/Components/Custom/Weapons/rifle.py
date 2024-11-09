import Scripts.Source.Components.Custom.Weapons.weapon as weapon_m
import Scripts.Source.Components.Default.transformation as transformation_m

NAME = 'Rifle'
DESCRIPTION = 'Rifle'


class Rifle(weapon_m.Weapon):
    def __init__(self, enable=True):
        super().__init__(10, 30, 3, 0.5, NAME, DESCRIPTION, enable)

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
