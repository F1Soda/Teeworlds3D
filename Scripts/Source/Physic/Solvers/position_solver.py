import glm

import Scripts.Source.Physic.Solvers.solver as solver_m


class PositionSolver(solver_m.Solver):
    def solve(self, collisions, dt):
        for collision in collisions:
            cp = collision.collide_point

            a_static = 1 if collision.physic_object_a.rigidbody and (not collision.physic_object_a.rigidbody.is_kinematic) else 0
            b_static = 1 if collision.physic_object_b.rigidbody and (not collision.physic_object_b.rigidbody.is_kinematic) else 0

            ta = collision.physic_object_a.collider.transformation
            tb = collision.physic_object_a.collider.transformation

            n = collision.collide_point.normal
            n = n / glm.length(n) * collision.collide_point.depth

            ta.pos = ta.pos + n * (1 - a_static)
            tb.pos = tb.pos - n * (1 - b_static)
