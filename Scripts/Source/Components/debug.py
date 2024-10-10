import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.transformation as transformation_m
import Scripts.Source.General.Managers.input_manager as input_manager_m
import glm
import pygame as pg

NAME = 'DEBUG'
DESCRIPTION = 'DEBUG'

UP = glm.vec3(0,1,0)

class Debug(component_m.Component):
    def __init__(self, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        input_manager_m.InputManager.handle_keyboard_press += self._handle_keyboard_press
        self.rigidbody = None
        self._transformation = None

    def _handle_keyboard_press(self, keys, pressed_char):
        if keys[pg.K_SPACE]:
            self.rigidbody.add_force(UP * 20)
        return True

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        self.rigidbody = self.rely_object.get_component_by_name("RigidBody")

    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def delete(self):
        input_manager_m.InputManager.handle_keyboard_press -= self._handle_keyboard_press

        self.app = None
        self.transformation = None
        self.rely_object = None
        self.rely_object = None
