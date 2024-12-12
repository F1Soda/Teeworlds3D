import Scripts.Source.Physic.Solvers.impulse_solver as impulse_solver_m
import Scripts.Source.Physic.Solvers.position_solver as position_solver_m
import glm


class PhysicObject:
    def __init__(self, rigidbody, collider):
        self.id = collider.rely_object.id
        self.rigidbody = rigidbody
        self.collider = collider

    def __str__(self):
        return f"Physic Object \"{self.collider.rely_object.name}\": Collider: {self.collider}, Rigidbody: {self.rigidbody}"


class Collision:
    def __init__(self, physic_object_a, physic_object_b, collide_point):
        self.physic_object_a = physic_object_a
        self.physic_object_b = physic_object_b
        self.collide_point = collide_point


class PhysicWorld:
    def __init__(self, game):
        self.level = None
        self.paused = False
        self.physic_objects, self.collide_objects, self.triggers = {}, {}, set()
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
        collider_component = game_object.get_component_by_name("Collider")
        rigidbody_component = game_object.get_component_by_name("RigidBody")
        if collider_component is None:
            raise Exception("Physic object should contain collider component!")

        physic_object = PhysicObject(rigidbody_component, collider_component)
        if physic_object.id in self.collide_objects.keys():
            return
        self.collide_objects[physic_object.id] = physic_object

        if collider_component.is_trigger:
            self.triggers.add(collider_component)
            self.triggered_colliders_enter[collider_component] = set()
            self.triggered_colliders_current_triggering[collider_component] = set()
            self.triggered_colliders_exit[collider_component] = set()

        if rigidbody_component and collider_component:
            if physic_object.id in self.physic_objects.keys():
                return
            self.physic_objects[physic_object.id] = physic_object
        elif rigidbody_component and not collider_component:
            raise Exception("If physic object contain Rigidbody, then it also should contain Collider!")

    def remove_object(self, game_object):
        # rigidbody_component = game_object.get_component_by_name("RigidBody")
        # collider_component = game_object.get_component_by_name("Collider")
        # if collider_component:
        #     self.collide_objects = [collider_component != x.collider for x in self.physic_objects]
        # if rigidbody_component:
        #     self.physic_objects = [rigidbody_component != x.rigidbody for x in self.physic_objects]
        if self.collide_objects.get(game_object.id):
            del self.collide_objects[game_object.id]
        if self.physic_objects.get(game_object.id):
            del self.physic_objects[game_object.id]

    def _resolve_constrains(self, dt):
        collisions = []
        for physic_object in self.physic_objects.values():
            if not physic_object.rigidbody.enable_with_rely_object:
                continue

            for collide_object in self.collide_objects.values():
                if (collide_object.collider.rely_object.id == physic_object.collider.rely_object.id or
                        collide_object.collider.is_trigger or not collide_object.collider.enable_with_rely_object):
                    continue

                d = glm.length(physic_object.collider.transformation.pos - collide_object.collider.transformation.pos)
                if d - physic_object.collider.max_radius_of_collisions - collide_object.collider.max_radius_of_collisions > 0:
                    continue

                collide_point = physic_object.collider.get_collide_point(collide_object.collider)

                if collide_point:
                    collisions.append(Collision(physic_object, collide_object.collider, collide_point))

        for trigger in self.triggers:
            if not trigger.enable_with_rely_object:
                continue
            for collide_object in self.collide_objects.values():
                if (collide_object.collider.rely_object.id == trigger.rely_object.id or
                        not collide_object.collider.enable_with_rely_object):
                    continue

                collide_with = trigger.collide_with(collide_object.collider)

                if collide_with:
                    if collide_object not in self.triggered_colliders_enter[trigger] and collide_object not in \
                            self.triggered_colliders_current_triggering[trigger]:
                        self.triggered_colliders_enter[trigger].add(collide_object)
                        self.triggered_colliders_current_triggering[trigger].add(collide_object)
                else:
                    if collide_object in self.triggered_colliders_current_triggering[trigger]:
                        self.triggered_colliders_exit[trigger].add(collide_object)
                        self.triggered_colliders_current_triggering[trigger].remove(collide_object)

        for trigger, collided_objects in self.triggered_colliders_enter.items():
            for collided_object in collided_objects:
                trigger.on_collision_enter(collided_object)
            self.triggered_colliders_enter[trigger].clear()

        for trigger, collided_objects in self.triggered_colliders_exit.items():
            for collided_object in collided_objects:
                trigger.on_collision_exit(collided_object)
            self.triggered_colliders_exit[trigger].clear()

        for solver in self.solvers:
            solver.solve(collisions, dt)

    def step(self, dt):
        if self.paused:
            return

        for physic_object in self.physic_objects.values():
            physic_object.rigidbody.apply_gravity()

        self._resolve_constrains(dt)

        for physic_object in self.physic_objects.values():
            physic_object.rigidbody.apply_forces_and_clear(dt)

    def init_physic_object_by_level(self, level):
        self.level = level

        for game_object in level.objects.values():
            self._init_game_object(game_object)

    def _init_game_object(self, game_object):
        collider_component = game_object.get_component_by_name("Collider")
        if collider_component is not None:
            self.add_object(game_object)

        for child in game_object.child_objects:
            self._init_game_object(child)

    def add_default_solvers(self):
        self.solvers.append(impulse_solver_m.ImpulseSolver())
        self.solvers.append(position_solver_m.PositionSolver())

    def _ray_cast_hit_cube(self, start, direction, mesh_filter) -> glm.vec3 | None:
        direction = direction / glm.length(direction)

        global_vertices = []
        for vertex in mesh_filter.mesh.vertices:
            global_vertex = mesh_filter.transformation.m_model * glm.vec4(vertex, 1)
            global_vertices.append(global_vertex.xyz)

        intersection_points = []

        for i in range(6):
            a, b, c = [global_vertices[index] for index in mesh_filter.mesh.indices[i * 2]]

            n = glm.cross(b - a, c - a)
            n_dot_d = glm.dot(n, direction)
            if abs(n_dot_d) < 10 ** -5:
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

        if len(intersection_points) == 0:
            return None

        min_point = intersection_points[0]
        for point in intersection_points:
            if glm.length(min_point - start) > glm.length(point - start):
                min_point = point

        return min_point

    @staticmethod
    def _point_in_triangle(p, a, b, c) -> bool:
        # Векторы для сторон треугольника
        v0 = c - a
        v1 = b - a
        v2 = p - a

        # Вычисление скалярных произведений
        dot00 = glm.dot(v0, v0)
        dot01 = glm.dot(v0, v1)
        dot02 = glm.dot(v0, v2)
        dot11 = glm.dot(v1, v1)
        dot12 = glm.dot(v1, v2)

        # Вычисление барицентрических координат
        denom = dot00 * dot11 - dot01 * dot01
        if denom == 0:
            return False  # точки a, b, c коллинеарны и не задают треугольник

        u = (dot11 * dot02 - dot01 * dot12) / denom
        v = (dot00 * dot12 - dot01 * dot02) / denom

        # Точка находится внутри треугольника, если u, v >= 0 и u + v <= 1
        return (u >= 0) and (v >= 0) and (u + v <= 1)

    def ray_cast_hit(self, start, direction) -> glm.vec3 | None:
        obj_id = self.game.object_picker.get_object_id_at_pos(self.game.win_size / 2)

        if obj_id != 0:
            obj = self.level.objects[obj_id]
            if mesh_filter := obj.get_component_by_name("Mesh Filter"):
                if mesh_filter.mesh.name == "cube":
                    return self._ray_cast_hit_cube(start, direction, mesh_filter)
        return None
