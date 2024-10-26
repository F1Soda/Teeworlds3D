import Scripts.Source.Physic.Solvers.solver as solver_m
import glm


class ImpulseSolver(solver_m.Solver):
    def solve(self, collisions, dt):
        for collision in collisions:
            # components rigidbodies if they exist on objects
            a_body = collision.physic_object_a.rigidbody
            b_body = collision.physic_object_b.rigidbody

            a_vel = a_body.velocity if a_body else glm.vec3()
            b_vel = b_body.velocity if b_body else glm.vec3()

            a_inv_mass = a_body.inv_mass if a_body else 0
            b_inv_mass = b_body.inv_mass if b_body else 0

            # collide point data contain normal and depth collision
            normal = collision.collide_point.normal

            # calculate impulse scalar
            e = min((a_body.restitution if a_body else 1), (b_body.restitution if b_body else 1))
            j = -(1 + e) * glm.dot(a_vel - b_vel, normal)
            j /= (a_inv_mass + b_inv_mass) * glm.dot(normal, normal)

            if (not a_body.is_kinematic) if a_body else False:
                a_body.velocity += j * a_inv_mass * normal

            if (not b_body.is_kinematic) if b_body else False:
                b_body.velocity -= j * a_inv_mass * normal
