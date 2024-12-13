import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m

NAME = 'Player'
DESCRIPTION = 'Player Component'


class Player(component_m.Component):
    def __init__(self, health=100, speed=2, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        self.health = health
        self.speed = speed
        self.max_length_hook = 10
        self.weapon = None
        self.in_hook_move = False
        self.player_controller = None
        self.rigidbody = None
        self.collider = None
        self.fps_camera_movement = None
        self.alive = True
        self._transformation = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)

    def apply(self):
        if self.transformation.pos.y < -50 and self.alive:
            self.app.level.send_kill_player("fall down")
            self.transformation.pos = self.transformation.pos

    def die(self):
        self.weapon.enable = False
        self.player_controller.enable = False
        self.rigidbody.enable = False
        self.collider.enable = False
        self.fps_camera_movement.enable = False
        self.alive = False

    def respawn(self):
        self.weapon.enable = True
        self.player_controller.enable = True
        self.rigidbody.enable = True
        self.rigidbody.clear_velocity()
        self.collider.enable = True
        self.fps_camera_movement.enable = True
        self.alive = True

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
        if self.weapon is not None:
            self.weapon.delete()

    def serialize(self) -> {}:
        return {
            "health": self.health,
            "pos": (self.transformation.pos.x, self.transformation.pos.y, self.transformation.pos.z),
            "rot": (self.transformation.rot.x, self.transformation.rot.y, self.transformation.rot.z)
        }
