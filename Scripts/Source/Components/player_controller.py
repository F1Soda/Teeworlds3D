import copy

import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.transformation as transformation_m
import Scripts.Source.General.Managers.input_manager as input_manager_m
import glm
import pygame as pg

NAME = "Player Controller"
DESCRIPTION = "Компонент для перемещения игрока"

SPEED = 0.05

VEC_UP = glm.vec3(0, 1, 0)


# forward = glm.vec3(-1, 0, 0)
# right = glm.vec3(0, 0, 1)


class PlayerController(component_m.Component):
    def __init__(self, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        input_manager_m.InputManager.handle_keyboard_press += self._handle_keyboard_press
        self._transformation = None
        self._rigidbody = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.transformation
        self._rigidbody = self.rely_object.get_component_by_name("Rigidbody")

    @property
    def rigidbody(self):
        if self._rigidbody is None:
            self._rigidbody = self.rely_object.get_component_by_name("RigidBody")
        return self._rigidbody

    def _move(self, keys):
        velocity = SPEED
        if keys[pg.K_w]:
            self.rigidbody.add_force(self.transformation.forward * 10)
        if keys[pg.K_s]:
            self.rigidbody.add_force(-self.transformation.forward * 10)
        if keys[pg.K_a]:
            self.rigidbody.add_force(-self.transformation.right * 10)
        if keys[pg.K_d]:
            self.rigidbody.add_force(self.transformation.right * 10)

        if keys[pg.K_SPACE]:
            self.rigidbody.add_force(self.transformation.up * 25)

    def apply(self):
        pass

    def _handle_keyboard_press(self, keys, pressed_char):
        self._move(keys)
        return True

    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def serialize(self) -> {}:
        return {
            'enable': self.enable
        }

    def delete(self):
        input_manager_m.InputManager.handle_keyboard_press -= self._handle_keyboard_press

        self.app = None
        self.transformation = None
        self.rely_object = None
