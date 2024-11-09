import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m
import Scripts.Source.General.Managers.input_manager as input_manager_m
import glm
import pygame as pg

NAME = "Player Controller"
DESCRIPTION = "Компонент для перемещения игрока"

VEC_UP = glm.vec3(0, 1, 0)


class PlayerController(component_m.Component):
    def __init__(self, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        input_manager_m.InputManager.handle_keyboard_press += self._handle_keyboard_press
        input_manager_m.InputManager.handle_left_click_event += self._handle_mouse_left_press
        self._transformation = None
        self._rigidbody = None
        self._player = None
        self.max_velocity = 10
        self.acceleration = 10
        self.can_move = True
        self.debug_box = None
        self.camera_component = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.transformation
        self._rigidbody = self.rely_object.get_component_by_name("Rigidbody")

    @property
    def player(self):
        if self._player is None:
            self._player = self.rely_object.get_component_by_name("Player")
        return self._player

    @property
    def rigidbody(self):
        if self._rigidbody is None:
            self._rigidbody = self.rely_object.get_component_by_name("RigidBody")
        return self._rigidbody

    def _move(self, keys):
        if not self.can_move:
            return

        if glm.length(self.rigidbody.velocity) <= self.max_velocity:
            if keys[pg.K_w]:
                self.rigidbody.add_force(self.transformation.forward * self.rigidbody.mass * self.acceleration)
            if keys[pg.K_s]:
                self.rigidbody.add_force(-self.transformation.forward * self.rigidbody.mass * self.acceleration)
            if keys[pg.K_a]:
                self.rigidbody.add_force(-self.transformation.right * self.rigidbody.mass * self.acceleration)
            if keys[pg.K_d]:
                self.rigidbody.add_force(self.transformation.right * self.rigidbody.mass * self.acceleration)

        if keys[pg.K_SPACE]:
            self.rigidbody.add_force(self.transformation.up * 20)

    def apply(self):
        pass

    def _handle_keyboard_press(self, keys, pressed_char):
        self._move(keys)
        return True

    def _handle_mouse_left_press(self, mouse_pos):
        if not self.player.in_hook_move:
            # поменять на камеру
            hit_point = self.app.physic_world.ray_cast_hit(self.camera_component.transformation.global_pos,
                                                           self.camera_component.transformation.forward)
            if hit_point:
                self.debug_box.transformation.pos = hit_point
                return True
        return False

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
