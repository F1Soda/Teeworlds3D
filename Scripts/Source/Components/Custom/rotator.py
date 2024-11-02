import Scripts.Source.Components.Default.component as component_m
import copy

NAME = "Rotator"
DESCRIPTION = "Rotate object by predefined ways"




class Rotator(component_m.Component):
    X = 0b001  # 1
    Y = 0b010  # 2
    Z = 0b100  # 4
    def __init__(self, speed=1, rotate_by=Y, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self.rotate_by = rotate_by
        self.speed = speed
        self.origin_angle = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self.origin_angle = copy.copy(self.rely_object.transformation.rot)

    def apply(self):
        if self.rotate_by & Rotator.X:
            self.rely_object.transformation.rot.x += self.speed
        if self.rotate_by & Rotator.Y:
            self.rely_object.transformation.rot.y += self.speed
        if self.rotate_by & Rotator.Z:
            self.rely_object.transformation.rot.z += self.speed
        self.rely_object.transformation.update_model_matrix()

    def serialize(self) -> {}:
        return {
            'speed': self.speed,
            'rotate_by': self.rotate_by,
            'enable': self.enable
        }
