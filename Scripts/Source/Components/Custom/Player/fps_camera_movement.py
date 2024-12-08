import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m
import Scripts.Source.General.Managers.input_manager as input_manager_m
import glm

NAME = "FPS Camera Movement"
DESCRIPTION = "Компонент для вращения камеры в игре"

SENSITIVITY = 0.15

VEC_UP = glm.vec3(0, 1, 0)


class FPSCameraMovement(component_m.Component):
    def __init__(self, player, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self._rel_pos = glm.vec2()
        self.player_transformation = player.transformation
        self.camera_component = None
        self._transformation = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.transformation
        self.camera_component = self.rely_object.get_component_by_name('Camera')  # type: camera_m.Camera

    def _rotate(self):
        mouse_dx, mouse_dy = input_manager_m.InputManager.mouse_diff
        new_rot_y = self.player_transformation.rot.y - mouse_dx * SENSITIVITY
        new_rot_x = self.transformation.rot.x - mouse_dy * SENSITIVITY
        new_rot_x = max(-89, min(89, new_rot_x))
        self.player_transformation.rot = (self.player_transformation.rot.x, new_rot_y, self.transformation.rot.z)
        self.transformation.rot = (new_rot_x, self.transformation.rot.y, self.transformation.rot.z)
        pass

    def apply(self):
        #print("FPS_CAMERA_MOVEMENT")
        self._rotate()
        #print("FPS_CAMERA_MOVEMENT_END")

    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def serialize(self) -> {}:
        # Удалить надо, этот компонент не будет сериализироваться
        return {
            'enable': self.enable
        }

    def delete(self):
        self.app = None
        self.camera_component = None
        self.transformation = None
        self.rely_object = None
