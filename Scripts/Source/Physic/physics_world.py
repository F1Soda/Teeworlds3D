import Scripts.Source.Physic.Solvers.impulse_solver as impulse_solver_m
import Scripts.Source.Physic.Solvers.position_solver as position_solver_m
import Scripts.Source.General.Managers.input_manager as input_manager_m
import glm


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
    def __init__(self, game):
        self.level = None
        self.paused = False
        self.physic_objects, self.collide_objects, self.triggers = [], [], []
        self.solvers = []
        self._collisions = []
        self.triggered_colliders_enter = {}
        self.triggered_colliders_exit = {}
        self.triggered_colliders_current_triggering = {}
        self.game = game

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
                if collide_object.collider.rely_object.id == physic_object.collider.rely_object.id or collide_object.collider.is_trigger:
                    continue

                collide_point = physic_object.collider.get_collide_point(collide_object.collider)

                if collide_point:
                    collisions.append(Collision(physic_object, collide_object.collider, collide_point))

        for trigger in self.triggers:
            for collide_object in self.collide_objects:
                if collide_object.collider.rely_object.id == trigger.rely_object.id:
                    continue

                collide_with = trigger.collide_with(collide_object.collider)

                if collide_with:
                    if collide_object not in self.triggered_colliders_enter[trigger]:
                        self.triggered_colliders_enter[trigger].append(collide_object)
                        self.triggered_colliders_current_triggering[trigger].append(collide_object)
                else:
                    if collide_object in self.triggered_colliders_current_triggering[trigger]:
                        self.triggered_colliders_exit[trigger].append(collide_object)
                        self.triggered_colliders_current_triggering[trigger].remove(collide_object)

        for trigger, collided_objects in self.triggered_colliders_enter.items():
            for collided_object in collided_objects:
                trigger.on_collision_enter(collided_object)
            self.triggered_colliders_enter[trigger] = []

        for trigger, collided_objects in self.triggered_colliders_exit.items():
            for collided_object in collided_objects:
                trigger.on_collision_exit(collided_object)
            self.triggered_colliders_exit[trigger] = []

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
            self._init_game_object(game_object)

    def _init_game_object(self, game_object):
        rigidbody_component = game_object.get_component_by_name("RigidBody")
        collider_component = game_object.get_component_by_name("Collider")
        if collider_component is not None:
            physic_object = PhysicObject(rigidbody_component, collider_component)
            self.collide_objects.append(physic_object)
            if rigidbody_component is not None and collider_component is not None:
                self.physic_objects.append(physic_object)

            if collider_component.is_trigger:
                self.triggers.append(collider_component)
                self.triggered_colliders_enter[collider_component] = []
                self.triggered_colliders_current_triggering[collider_component] = []
                self.triggered_colliders_exit[collider_component] = []

        for child in game_object.child_objects:
            self._init_game_object(child)

    def add_default_solvers(self):
        self.solvers.append(impulse_solver_m.ImpulseSolver())
        self.solvers.append(position_solver_m.PositionSolver())

    def _ray_cast_hit_cube(self, start, direction, mesh_filter) -> glm.vec3:
        direction = direction / glm.length(direction)

        global_vertices = []
        for vertex in mesh_filter.mesh.vertices:
            global_vertex = mesh_filter.transformation.m_model * glm.vec4(vertex, 1)
            global_vertices.append(global_vertex.xyz)

        intersection_points = []

        for i in range(6):
            a, b, c = [global_vertices[index] for index in mesh_filter.mesh.indices[i * 2]]

            n = glm.cross(b - a, c - a)
            if abs(n_dot_d := glm.dot(n, direction)) < 10 ** -5:
                continue

            t = glm.dot(n, a - start) / n_dot_d

            if t < 0:
                continue

            point_on_plane = start + t * direction

            if self._point_in_triangle(point_on_plane, a, b, c):
                intersection_points.append(point_on_plane)
            else:
                a, b, c = [global_vertices[index] for index in mesh_filter.mesh.indices[i * 2 + 1]]
                if self._point_in_triangle(point_on_plane, a, b, c):
                    intersection_points.append(point_on_plane)

        min_point = intersection_points[0]
        for point in intersection_points:
            if glm.length(min_point-start) > glm.length(point-start):
                min_point = point

        return min_point

    @staticmethod
    def _point_in_triangle(p, a, b, c) -> bool:
        # Compute vectors
        ac = a - c
        ab = a - b
        area_abc = glm.length(glm.cross(ab, ac)) / 2

        pa = p - a
        pb = p - b
        pc = p - c

        alpha = glm.length(glm.cross(pb, pc)) / (2 * area_abc)
        betta = glm.length(glm.cross(pc, pa)) / (2 * area_abc)
        gamma = 1 - alpha - betta

        return 0 <= alpha <= 1 and 0 <= betta <= 1 and abs(alpha + betta + gamma - 1) <= 10**-3

    def ray_cast_hit(self, start, direction) -> glm.vec3 | None:
        obj_id = self.game.object_picker.get_object_id_at_pos(self.game.win_size/2)

        if obj_id != 0:
            obj = self.level.objects[obj_id]
            if mesh_filter := obj.get_component_by_name("Mesh Filter"):
                if mesh_filter.mesh.name == "cube":
                    return self._ray_cast_hit_cube(start, direction, mesh_filter)
        return None
