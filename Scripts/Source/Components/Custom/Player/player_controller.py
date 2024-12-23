import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m
import Scripts.Source.General.Managers.input_manager as input_manager_m
import enum
import glm
import pygame as pg

NAME = "Player Controller"
DESCRIPTION = "Компонент для перемещения игрока"

VEC_UP = glm.vec3(0, 1, 0)


class PlayerState(enum.Enum):
    Normal = 0
    HookshotFlyingPlayer = 1
    HookShotThrown = 2


class PlayerController(component_m.Component):
    def __init__(self, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        # input_manager_m.InputManager.handle_keyboard_press += self._handle_keyboard_press
        input_manager_m.InputManager.handle_right_click_event += self._handle_mouse_right_press
        input_manager_m.InputManager.handle_left_click_event += self._handle_mouse_left_press
        input_manager_m.InputManager.handle_left_hold_event += self._handle_mouse_left_press

        self.state = PlayerState.Normal

        self._transformation = None
        self._rigidbody = None
        self._player = None
        self.max_velocity = 10
        self.acceleration = 40
        self.hookshot_speed = 0
        self.can_move = True
        self.debug_box = None

        self._hookshot_position = glm.vec3()
        self._hookshot_size = 0

        self.camera_component = None
        self.hookshot_transformation = None
        self.hookshot_model_transformation = None
        self.weapon_component = None
        self.in_jump = False

        self.cheats_is_bad_but_for_project_i_need_do_that = False

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.transformation
        self._rigidbody = self.rely_object.get_component_by_name("Rigidbody")

        self.rely_object.components_to_apply_fixed_update.append(self)

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
        if not self.can_move or self.state == PlayerState.HookshotFlyingPlayer:
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
            self._jump()

    def _jump(self, height_coefficient=160):
        # if self.in_jump:
        #     return
        self.rigidbody.add_force(self.transformation.up * height_coefficient)
        self.in_jump = True

    def apply(self):
        # print("PLAYER_CONTROLLER")
        if self.state in [self.state.HookshotFlyingPlayer, PlayerState.HookShotThrown]:
            self.hookshot_dir = glm.normalize(self._hookshot_position - self.transformation.pos)
            if self.state == self.state.HookshotFlyingPlayer:
                self.move_hookshot()
            elif self.state == PlayerState.HookShotThrown:
                self.hookshot_start()
        # else:
        #     if self.camera_component:
        #         self.hookshot_transformation.forward = self.camera_component.transformation.forward
        # print("PLAYER_CONTROLLER_END")

    def fixed_apply(self):
        self._handle_keyboard_press(input_manager_m.InputManager.keys)

    def hookshot_start(self):
        hookshot_throw_speed = 40
        self._hookshot_size += hookshot_throw_speed * self.app.delta_time

        if self._hookshot_size >= glm.length(self._hookshot_position - self.transformation.pos):
            self.state = PlayerState.HookshotFlyingPlayer

        self.hookshot_transformation.forward = self.hookshot_dir
        self.hookshot_transformation.scale = glm.vec3(1, 1, self._hookshot_size)

    def hookshot_stop(self):
        self.hookshot_transformation.scale = glm.vec3(1)
        self.hookshot_transformation.rot = glm.vec3(0)
        self.hookshot_model_transformation.pos = glm.vec3(0, 0, 0.5)
        self.hookshot_model_transformation.rot = glm.vec3(0)
        self.hookshot_model_transformation.rely_object.enable = False

    def _handle_keyboard_press(self, keys):
        if not self.enable_with_rely_object:
            return

        if keys[pg.K_SPACE] and self.state == PlayerState.HookshotFlyingPlayer:
            self.state = PlayerState.Normal
            self._jump(100)
            self.can_move = False
            self.rigidbody.use_gravity = True
            self.hookshot_stop()
            self.rigidbody.velocity = self.hookshot_dir * self.hookshot_speed
        self._move(keys)
        if keys[pg.K_r]:
            self.weapon_component.reload()
        if keys[pg.K_p]:
            self.cheats_is_bad_but_for_project_i_need_do_that = not self.cheats_is_bad_but_for_project_i_need_do_that
            self.app.level.set_cheats(self.cheats_is_bad_but_for_project_i_need_do_that)

        return True

    def _handle_mouse_right_press(self, mouse_pos):
        if not self.enable_with_rely_object:
            return

        hit_point = self.app.physic_world.ray_cast_hit(self.camera_component.transformation.global_pos,
                                                       self.camera_component.transformation.forward)
        if hit_point:
            self.state = PlayerState.HookShotThrown
            self._hookshot_position = hit_point
            self.hookshot_dir = glm.normalize(hit_point - self.transformation.pos)
            self._hookshot_size = 0
            self.debug_box.transformation.pos = hit_point
            # print("START FLY")
            self.hookshot_model_transformation.rely_object.enable = True
            return True
        return False

    def _handle_mouse_left_press(self, mouse_pos):
        if not self.enable_with_rely_object:
            return
        self.weapon_component.fire()
        return True

    def move_hookshot(self):
        self.rigidbody.use_gravity = False
        self.hookshot_distance = glm.length(self._hookshot_position - self.transformation.pos)
        hookshot_speed_max = 40
        hookshot_speed_min = 10
        self.hookshot_speed = glm.clamp(glm.length(self.hookshot_distance), hookshot_speed_min, hookshot_speed_max)
        hookshot_speed_multiplier = 2

        self.transformation.pos = self.transformation.pos + self.hookshot_dir * hookshot_speed_multiplier * self.hookshot_speed * self.app.delta_time
        self.hookshot_transformation.forward = self.hookshot_dir
        self.hookshot_transformation.scale = glm.vec3(1, 1, self.hookshot_distance)
        reached_hookshot_position_distance = 1
        if self.hookshot_distance < reached_hookshot_position_distance:
            self.state = PlayerState.Normal
            self.rigidbody.use_gravity = True
            self.hookshot_stop()

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
