import Scripts.Source.Physic.Solvers.solver as solver_m
import glm


class ImpulseSolver(solver_m.Solver):
    def solve(self, collisions, dt):
        for collision in collisions:
            n = collision.collide_point.normal
            n = n / glm.length(n)

            # components rigidbodies if they exist on objects
            a_body = collision.physic_object_a.rigidbody
            b_body = collision.physic_object_b.rigidbody

            a_vel = a_body.velocity if a_body else glm.vec3()
            b_vel = b_body.velocity if b_body else glm.vec3()

            a_inv_mass = a_body.inv_mass if a_body else 0
            b_inv_mass = b_body.inv_mass if b_body else 0

            r_vel = a_vel - b_vel

            # calculate impulse scalar
            e = min((a_body.restitution if a_body else 1), (b_body.restitution if b_body else 1))
            j = -(1 + e) * glm.dot(r_vel, n)
            j /= (a_inv_mass + b_inv_mass)

            if (not a_body.is_kinematic) if a_body else False:
                a_vel += j * a_inv_mass * n

            if (not b_body.is_kinematic) if b_body else False:
                b_vel -= j * a_inv_mass * n

            # Friction

            r_vel = a_vel - b_vel
            n_spd = glm.dot(r_vel, n)

            tangent = r_vel - n_spd * n
            if glm.length(tangent) > 0.0001:
                tangent /= glm.length(tangent)

            f_vel = glm.dot(r_vel, tangent)

            a_sf = a_body.static_friction if a_body else 1
            b_sf = b_body.static_friction if b_body else 1
            a_df = a_body.dynamic_friction if a_body else 1
            b_df = b_body.dynamic_friction if b_body else 1
            mu = pow(a_sf * a_sf + b_sf * b_sf, 0.5)

            jt = -glm.dot(r_vel, tangent)
            jt /= (a_inv_mass + b_inv_mass)

            if abs(jt) <= j * mu:
                friction = jt * tangent
            else:
                mu = pow(a_df * a_df + b_df * b_df, 0.5)
                friction = -j * tangent * mu

            if (not a_body.is_kinematic) if a_body else False:
                a_body.velocity = a_vel - friction * a_inv_mass

            if (not b_body.is_kinematic) if b_body else False:
                b_body.velocity = b_vel + friction * b_inv_mass
