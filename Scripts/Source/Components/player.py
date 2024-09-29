import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.transformation as transformation_m

NAME = 'Player'
DESCRIPTION = 'Player Component'


class Player(component_m.Component):
    def __init__(self, health=100, speed=2, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        self.health = health
        self.speed = speed
        self.weapon = None

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
        self.weapon.delete()

    def serialize(self) -> {}:
        # Тоже не сериализуемый класс
        return {
            "health": 100,
            'speed': 2
        }
