import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m
import glm

NAME = 'Bullet'
DESCRIPTION = 'Bullet'

VEC_ZERO = glm.vec3(0)


class Bullet(component_m.Component):
    def __init__(self, velocity: float, action_after_life_time, life_time=4):
        super().__init__(NAME, DESCRIPTION, True)

        self.velocity = velocity
        self.life_time = life_time
        self.action_after_life_time = action_after_life_time
        self.elapsed_time = 0
        self.direction = VEC_ZERO
        self._transformation = None
        self.trigger = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)

        self.rely_object.components_to_apply_fixed_update.append(self)
        self.trigger = self.rely_object.get_component_by_name("Collider")
        self.trigger.on_collision_enter += self.on_trigger_enter

    def on_trigger_enter(self, collider_obj):
        if collider_obj.collider.rely_object.name == "Player":
            return
        print(
            f"Bullet_{self.rely_object.id}_{self.rely_object.enable} collided with {collider_obj.collider.rely_object.name}")
        self.action_after_life_time(self)
        self.elapsed_time = 0


    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def fixed_apply(self):
        self.transformation.pos = (self.transformation.pos +
                                   self.direction * self.velocity * self.app.fixed_delta_time)
        self.elapsed_time += self.app.fixed_delta_time
        if self.elapsed_time > self.life_time or glm.length(self.transformation.pos) > 50:
            self.action_after_life_time(self)
            self.elapsed_time = 0

    def delete(self):
        self._transformation = None
        self.rely_object = None

    def serialize(self) -> {}:
        return {
            "pos": (
                self.transformation.global_pos.x, self.transformation.global_pos.y, self.transformation.global_pos.z),
            "rot": (self.transformation.rot.x, self.transformation.rot.y, self.transformation.rot.z)
        }
