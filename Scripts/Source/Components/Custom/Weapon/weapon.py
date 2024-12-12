import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m
import Scripts.Source.General.ObjectsPool.pool_base as pool_base_m
import Scripts.Source.General.Managers.object_creator as object_creator_m
import Scripts.Source.Components.Custom.Weapon.bullet as bullet_m
import glm

NAME = 'Weapon'
DESCRIPTION = 'Weapon'


class Weapon(component_m.Component):
    def __init__(self, damage, magazine_size, reload_time, fire_rate, pool_object, camera_transformation,
                 name=NAME, description=DESCRIPTION,
                 enable=True):
        super().__init__(name, description, enable)

        self.damage = damage
        self.magazine_size = magazine_size
        self.reload_time = reload_time
        self.fire_rate = fire_rate
        self.pool_object = pool_object
        self.last_shot_time = 0

        self.camera_transformation = camera_transformation

        def before_return_func_bullet(b_c):
            b_c.rely_object.enable = False

        def preload_func_bullet():
            def action_after_bullet_lifetime(b_c):
                self.bullet_pool.back_to_pool(b_c)

            bullet = object_creator_m.ObjectCreator.create_bullet(pool_object)
            component = bullet.add_component(bullet_m.Bullet(1, action_after_bullet_lifetime))
            self.app.level.add_object(bullet)
            return component

        def get_func_bullet(b_c):
            b_c.rely_object.enable = True

        self.bullet_pool = pool_base_m.PoolBase(0, preload_func_bullet, get_func_bullet, before_return_func_bullet)

        self._transformation = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)

    def fire(self):
        if self.app.time - self.last_shot_time < self.fire_rate:
            return
        self.last_shot_time = self.app.time
        b_c = self.bullet_pool.get()
        b_c.transformation.pos = self.camera_transformation.global_pos
        b_c.transformation.forward = self.camera_transformation.forward.xyz
        b_c.direction = self.camera_transformation.forward.xyz

    def reload(self):
        ...

    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def apply(self):
        # if self.camera_transformation:
        self.transformation.forward = self.camera_transformation.forward
        # pass

    def delete(self):
        self._transformation = None
        self.rely_object = None

    def serialize(self) -> {}:
        ...
