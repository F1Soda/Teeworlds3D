import Scripts.Source.Physic.Solvers.solver as solver_m
import glm


class SmoothPositionSolver(solver_m.Solver):
    def solve(self, collisions, dt):
        deltas = []

        for collision in collisions:
            a_body = collision.physic_object_a.rigidbody
            b_body = collision.physic_object_b.rigidbody

            a_inv_mass = a_body.inv_mass if a_body else 0
            b_inv_mass = b_body.inv_mass if b_body else 0

            percent = 0.8
            slop = 0.01

            correction = collision.collide_point.normal * percent * max(
                collision.collide_point.penetration_depth - slop, 0.0) / (a_inv_mass + b_inv_mass)

            delta_a = a_inv_mass * correction if a_body and a_body.is_simulated else glm.vec3(0.0)
            delta_b = b_inv_mass * correction if b_body and a_body.is_simulated else glm.vec3(0.0)

            deltas.append((delta_a, delta_b))

        for i in range(len(collisions)):
            a_body = collisions[i].physic_object_a.rigidbody
            b_body = collisions[i].physic_object_b.rigidbody

            if a_body and a_body.is_simulated:
                a_body.transformation.pos -= deltas[i][0]

            if b_body and b_body.is_simulated:
                b_body.transformation.pos += deltas[i][1]
