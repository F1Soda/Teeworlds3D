import Scripts.Source.Physic.Solvers.impulse_solver as impulse_solver_m
import Scripts.Source.Physic.Solvers.position_solver as position_solver_m
import Scripts.Source.Physic.Solvers.smooth_position_solver as smooth_position_solver_m


class PhysicObject:
    def __init__(self, rigidbody, collider):
        self.rigidbody = rigidbody
        self.collider = collider


class Collision:
    def __init__(self, physic_object_a, physic_object_b, collide_point):
        self.physic_object_a = physic_object_a
        self.physic_object_b = physic_object_b
        self.collide_point = collide_point


class PhysicWorld:
    def __init__(self):
        self.level = None
        self.paused = False
        self.physic_objects, self.collide_objects = [], []
        self.solvers = []
        self._collisions = []

    def add_solver(self, solver):
        self.solvers.append(solver)

    def remove_solver(self, solver):
        self.solvers.remove(solver)

    def add_object(self, game_object):
        collider_component = game_object.get_component_by_name("Mesh Collider")
        if collider_component is None:
            raise Exception("Physic object should contain collider component!")
        self.collide_objects.append(collider_component)
        rigidbody_component = game_object.get_component_by_name("RigidBody")
        if rigidbody_component:
            self.physic_objects.append(PhysicObject(rigidbody_component, collider_component))

    def remove_object(self, game_object):
        rigidbody_component = game_object.get_component_by_name("RigidBody")
        collider_component = game_object.get_component_by_name("Mesh Collider")
        if collider_component:
            self.collide_objects = [collider_component != x.collider for x in self.physic_objects]
        if rigidbody_component:
            self.physic_objects = [rigidbody_component != x.rigidbody for x in self.physic_objects]

    def _resolve_constrains(self, dt):
        collisions = []
        for physic_object in self.physic_objects:
            if not physic_object.rigidbody.enable:
                continue

            for collide_object in self.collide_objects:
                if collide_object.collider.rely_object.id == physic_object.collider.rely_object.id:
                    continue

                collide_point = physic_object.collider.get_collide_point(collide_object.collider)

                if collide_point:
                    collisions.append(Collision(physic_object, collide_object.collider, collide_point))

        for solver in self.solvers:
            solver.solve(collisions, dt)

    def step(self, dt):
        if self.paused:
            return

        for physic_object in self.physic_objects:
            physic_object.rigidbody.apply_gravity()

        self._resolve_constrains(dt)

        for physic_object in self.physic_objects:
            physic_object.rigidbody.apply_forces_and_clear(dt)

    def init_physic_object_by_level(self, level):
        self.level = level

        for game_object in level.objects.values():
            rigidbody_component = game_object.get_component_by_name("RigidBody")
            collider_component = game_object.get_component_by_name("Collider")
            if collider_component is not None:
                physic_object = PhysicObject(rigidbody_component, collider_component)
                self.collide_objects.append(physic_object)
                if rigidbody_component is not None and collider_component is not None:
                    self.physic_objects.append(physic_object)

    def add_default_solvers(self):
        self.solvers.append(impulse_solver_m.ImpulseSolver())
        self.solvers.append(position_solver_m.PositionSolver())
