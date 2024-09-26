import copy

import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.camera as camera_m
import Scripts.Source.Components.transformation as transformation_m
import Scripts.Source.General.Managers.input_manager as input_manager_m
import glm
import pygame as pg

NAME = "Free Fly Move"
DESCRIPTION = "Компонент для свободного передвижения камеры"

SPEED = 0.005
SHIFT_SPEED = 0.03
SENSITIVITY = 0.2

VEC_UP = glm.vec3(0, 1, 0)

class FreeFlyMove(component_m.Component):
    def __init__(self, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self.RIGHT_MOUSE_BUTTON_RELEASED = False
        input_manager_m.InputManager.handle_right_hold_event += self._handle_right_hold
        input_manager_m.InputManager.handle_right_release_event += self._handle_right_release
        input_manager_m.InputManager.handle_keyboard_press += self._handle_keyboard_press
        self._rel_pos = (0, 0)

        self.camera_component = None
        self._transformation = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.transformation
        self.camera_component = self.rely_object.get_component_by_name('Camera')  # type: camera_m.Camera

    def _move(self, keys):
        velocity = (SHIFT_SPEED if keys[pg.K_LSHIFT] else SPEED) * self.app.delta_time

        if keys[pg.K_w]:
            self.transformation.pos -= self.camera_component.forward * velocity
        if keys[pg.K_s]:
            self.transformation.pos += self.camera_component.forward * velocity
        if keys[pg.K_a]:
            self.transformation.pos -= self.camera_component.right * velocity
        if keys[pg.K_d]:
            self.transformation.pos += self.camera_component.right * velocity
        if keys[pg.K_q]:
            self.transformation.pos += self.camera_component.up * velocity
        if keys[pg.K_e]:
            self.transformation.pos -= self.camera_component.up * velocity

    def _rotate(self, mouse_pos):
        if not self.RIGHT_MOUSE_BUTTON_RELEASED:
            self.RIGHT_MOUSE_BUTTON_RELEASED = True
            self._rel_pos = mouse_pos
        rel_x = mouse_pos.x - self._rel_pos.x
        rel_y = self._rel_pos.y - mouse_pos.y
        self.transformation.rot.y += rel_x * SENSITIVITY
        self.transformation.rot.x -= rel_y * SENSITIVITY
        self.transformation.rot.x = max(-89, min(89, self.transformation.rot.x))
        self._rel_pos = copy.copy(mouse_pos)

    def apply(self):
        self._update_camera_vectors()

    def _handle_right_hold(self, mouse_pos):
        self._rotate(mouse_pos)
        return True

    def _handle_keyboard_press(self, keys, pressed_char):
        self._move(keys)
        return True

    def _handle_right_release(self, mouse_pos):
        self.RIGHT_MOUSE_BUTTON_RELEASED = False
        return True

    def _update_camera_vectors(self):
        x, y = glm.radians(self.transformation.rot.y), glm.radians(self.transformation.rot.x)

        self.camera_component.forward.x = glm.cos(x) * glm.cos(y)
        self.camera_component.forward.y = glm.sin(y)
        self.camera_component.forward.z = glm.sin(x) * glm.cos(y)

        self.camera_component.forward = glm.normalize(-self.camera_component.forward)
        self.camera_component.right = glm.normalize(glm.cross(VEC_UP, self.camera_component.forward))
        self.camera_component.up = glm.cross(self.camera_component.forward, self.camera_component.right)

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
        input_manager_m.InputManager.handle_right_hold_event -= self._handle_right_hold
        input_manager_m.InputManager.handle_right_release_event -= self._handle_right_release
        input_manager_m.InputManager.handle_keyboard_press -= self._handle_keyboard_press

        self.app = None
        self.camera_component = None
        self.transformation = None
        self.rely_object = None
