import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m
import Scripts.Source.General.Game.object as object_m

NAME = 'Ground Checker'
DESCRIPTION = 'Enable or disable move on the ground or above it'


class GroundChecker(component_m.Component):
    def __init__(self, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        self._transformation = None
        self.trigger = None
        self.player_controller = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        # self.player_controller = self.rely_object.parent_object.get_component_by_name("Player Controller")
        self.player_controller = self.rely_object.get_component_by_name("Player Controller")

    def set_collider(self, collider):
        self.trigger = collider
        self.trigger.is_trigger = True
        self.trigger.on_collision_enter += self.on_trigger_enter
        self.trigger.on_collision_exit += self.on_trigger_exit

    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def on_trigger_enter(self, collider_obj):
        # print(f"ENTER: {collider_obj.collider.rely_object.name}")

        if collider_obj.collider.rely_object.tag != object_m.Tags.Ground:
            return
        self.player_controller.can_move = True
        self.player_controller.in_jump = False
        print(f"CAN MOVE = TRUE, {collider_obj.collider.rely_object.name}")

    def on_trigger_exit(self, collider_obj):
        #print(f"EXIT: {collider_obj.collider.rely_object.name}")
        if collider_obj.collider.rely_object.tag != object_m.Tags.Ground:
            return
        self.player_controller.can_move = False
        print(f"CAN MOVE = FALSE, {collider_obj.collider.rely_object.name}")

    def delete(self):
        self._transformation = None
        self.rely_object = None

    def serialize(self) -> {}:
        # Тоже не сериализуемый класс
        return {
            "enable": True
        }
