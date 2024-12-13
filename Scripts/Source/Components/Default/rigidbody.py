import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m
import glm

NAME = 'RigidBody'
DESCRIPTION = 'Physics'

gravity = glm.vec3(0, -1, 0) * 9.8


class RigidBody(component_m.Component):
    def __init__(self, mass, is_kinematic=False, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self.mass = mass

        self.force = glm.vec3()
        self.velocity = glm.vec3()

        # params
        self.use_gravity = True
        self.is_kinematic = is_kinematic  # is_kinematic = True <=> object pos controlled by script
        self.restitution = 0.2  # Elasticity of collisions
        self.inv_mass = 1 / self.mass if mass != 0 else 1  # 1 / Mass of rigidbody

        self.static_friction = 0.8  # Static friction coefficient
        self.dynamic_friction = 0.4  # Dynamic friction coefficient

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

    def apply_impulse(self, impulse):
        self.velocity += impulse / self.mass

    def add_force(self, add_force):
        if not self.enable_with_rely_object:
            return
        self.force = self.force + add_force
        # ApplyTorque(glm::cross(position, force));

    def apply_gravity(self):
        if not self.enable_with_rely_object:
            return
        if self.use_gravity and self.mass > 0 and not self.is_kinematic:
            self.add_force(gravity * self.mass)

    def apply_forces_and_clear(self, dt):
        print(self.force)
        if not self.enable_with_rely_object:
            return
        if glm.length(self.velocity) > 10 * -5:
            self.velocity = self.velocity + self.force / self.mass * dt
            self.transformation.pos = self.transformation.pos + self.velocity * dt
        else:
            self.velocity = glm.vec3()
        # Очень плохо
        self.force = glm.vec3(0)

    def clear_force(self):
        self.force = glm.vec3(0)

    def clear_velocity(self):
        self.velocity = glm.vec3(0)

    def fixed_apply(self):
        pass

    def delete(self):
        self._transformation = None
        self.rely_object = None

    def serialize(self) -> {}:
        return {
            "mass": self.mass,
            'enable': self.enable
        }
