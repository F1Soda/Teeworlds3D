import Scripts.Source.Physic.Solvers.solver as solver_m


class PositionSolver(solver_m.Solver):
    def solve(self, collisions, dt):
        for collision in collisions:
            cp = collision.collide_point

            a_static = 1 if collision.physic_object_a.rigidbody and not collision.physic_object_a.rigidbody.is_simulated else 0
            b_static = 1 if collision.physic_object_b.rigidbody and not collision.physic_object_b.rigidbody.is_simulated else 0

            resolution = cp.normal * cp.penetration_depth / max(1, a_static + b_static)

            ta = collision.physic_object_a.collider.transformation
            tb = collision.physic_object_a.collider.transformation

            ta.pos = ta.pos - resolution * (1 - a_static)
            tb.pos = tb.pos + resolution * (1 - b_static)
