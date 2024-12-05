import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m

NAME = 'Client Wrapper'
DESCRIPTION = 'Client Wrapper'


class ClientWrapper(component_m.Component):
    def __init__(self, health=100, speed=2, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        self.health = health
        self.speed = speed
        self.in_hook_move = False

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
            "health": self.health,
            "pos": self.transformation.pos
        }
