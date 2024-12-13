import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m
import Scripts.Source.General.ObjectsPool.pool_base as pool_base_m
import Scripts.Source.General.Managers.object_creator as object_creator_m
import Scripts.Source.Components.Custom.Weapon.bullet as bullet_m

NAME = 'Client Weapon'
DESCRIPTION = 'Client Weapon'


class ClientWeapon(component_m.Component):
    def __init__(self, pool_object, name=NAME, description=DESCRIPTION, enable=True):
        super().__init__(name, description, enable)

        self.pool_object = pool_object

        self.elapsed_time_for_reloading = 0

        def before_return_func_bullet(b_c):
            b_c.rely_object.enable = False

        def preload_func_bullet():
            def action_after_bullet_lifetime(b_c):
                self.bullet_pool.back_to_pool(b_c)

            bullet = object_creator_m.ObjectCreator.create_bullet(pool_object)
            component = bullet.add_component(bullet_m.Bullet(15, action_after_bullet_lifetime))
            self.app.physic_world.add_object(bullet)
            return component

        def get_func_bullet(b_c):
            b_c.rely_object.enable = True

        self.bullet_pool = pool_base_m.PoolBase(0, preload_func_bullet, get_func_bullet, before_return_func_bullet)

        self._transformation = None

        self.id_owner = -1

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)

        self.id_owner = self.rely_object.id

    def fire(self, velocity, direction, start_pos):
        b_c = self.bullet_pool.get()
        b_c.transformation.pos = start_pos
        b_c.transformation.forward = direction
        b_c.direction = b_c.transformation.forward.xyz
        b_c.velocity = velocity
        b_c.id_owner = self.id_owner

    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def delete(self):
        self.bullet_pool.back_to_pool_all()
        for bullet in self.bullet_pool.pool:
            bullet.rely_object.delete()

        self.bullet_pool.pool.clear()

        self._transformation = None
        self.rely_object = None


    def serialize(self) -> {}:
        ...
