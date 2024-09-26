import Scripts.Source.Components.component as component_m
import glm
import enum
import copy

NAME = "Translator"
DESCRIPTION = "Translate object by predefined ways"


class Translator(component_m.Component):
    Circle = 0
    UpDown = 1
    LeftRight = 2
    CircleZY = 3
    ForwardBackward = 4

    def __init__(self, speed=2, radius=1, translate_by=Circle, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self.translate_by = translate_by
        self.radius = radius
        self.speed = speed
        self.center = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self.center = copy.copy(self.rely_object.transformation.pos)

    def apply(self):
        if self.translate_by == Translator.Circle:
            self.rely_object.transformation.pos.x = self.center.x + self.radius * glm.sin(self.app.time * self.speed)
            self.rely_object.transformation.pos.z = self.center.z + self.radius * glm.cos(self.app.time * self.speed)
        elif self.translate_by == Translator.UpDown:
            self.rely_object.transformation.pos.y = self.center.y + self.radius * glm.sin(self.app.time * self.speed)
        elif self.translate_by == Translator.LeftRight:
            self.rely_object.transformation.pos.z = self.center.z + self.radius * glm.sin(self.app.time * self.speed)
        elif self.translate_by == Translator.CircleZY:
            self.rely_object.transformation.pos.y = self.center.y + self.radius * glm.sin(self.app.time * self.speed)
            self.rely_object.transformation.pos.z = self.center.z + self.radius * glm.cos(self.app.time * self.speed)
        elif self.translate_by == Translator.ForwardBackward:
            self.rely_object.transformation.pos.x = self.center.x + self.radius * glm.sin(self.app.time * self.speed)
        self.rely_object.transformation.update_model_matrix()

    def serialize(self) -> {}:
        return {
            'speed': self.speed,
            'radius': self.radius,
            'translate_by': self.translate_by,
            'enable': self.enable
        }
