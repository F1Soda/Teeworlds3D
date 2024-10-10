import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.transformation as transformation_m
import Scripts.Source.General.Managers.physic_manager as physic_manager_m
import glm

NAME = 'RigidBody'
DESCRIPTION = 'Physics'


class RigidBody(component_m.Component):
    def __init__(self, mass, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self.mass = mass
        self.force = glm.vec3()
        self.velocity = glm.vec3()

        # params
        self.use_gravity = True

        self._transformation = None

    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)

    def add_force(self, add_force):
        self.force = self.force + add_force

    def fixed_apply(self):
        dt = self.app.delta_time
        if dt <= 0:
            return
        if self.use_gravity and self.mass > 0:
            self.force = self.force + self.mass * physic_manager_m.PhysicManager.GRAVITY
            self.velocity = self.velocity + self.force / self.mass * dt
            self.transformation.pos = self.transformation.pos + self.velocity * dt
            # Очень плохо
            self.force = glm.vec3(0)


    def delete(self):
        self._transformation = None
        self.rely_object = None

    def serialize(self) -> {}:
        return {
            "mass": self.mass,
            'enable': self.enable
        }
