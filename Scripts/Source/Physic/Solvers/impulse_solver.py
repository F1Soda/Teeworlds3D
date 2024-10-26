import Scripts.Source.Physic.Solvers.solver as solver_m
import glm


class ImpulseSolver(solver_m.Solver):
    def solve(self, collisions, dt):
        for collision in collisions:
            a_body = collision.physic_object_a.rigidbody
            b_body = collision.physic_object_b.rigidbody

            # collision.physic_object_a.collider.transformation.pos = (
            #     collision.physic_object_a.collider.transformation.pos - collision.collide_point.normal * collision.collide_point.penetration_depth)
            # if a_body:
            #     a_body.velocity = glm.vec3(0)

            a_vel = a_body.velocity if a_body else glm.vec3()
            b_vel = b_body.velocity if b_body else glm.vec3()
            r_vel = b_vel - a_vel
            n_spd = glm.dot(r_vel, collision.collide_point.normal)

            a_inv_mass = a_body.inv_mass if a_body else 1
            b_inv_mass = b_body.inv_mass if b_body else 1

            # Impulse

            if n_spd >= 0:
                continue

            e = (a_body.restitution if a_body else 1) * (b_body.restitution if b_body else 1)

            j = -(1 + e) * n_spd / (a_inv_mass + b_inv_mass)

            impulse = j * collision.collide_point.normal

            if a_body.is_simulated if a_body else False:
                a_vel -= impulse * a_inv_mass

            if b_body.is_simulated if b_body else False:
                b_vel += impulse * b_inv_mass

            # Friction

            r_vel = b_vel - a_vel
            n_spd = glm.dot(r_vel, collision.collide_point.normal)

            tangent = r_vel - n_spd * collision.collide_point.normal

            if glm.length(tangent) > 0.0001:
                tangent = glm.normalize(tangent)

            f_vel = glm.dot(r_vel, tangent)

            aSF = a_body.static_friction if a_body else 0
            bSF = b_body.static_friction if b_body else 0
            aDF = a_body.dynamic_friction if a_body else 0
            bDF = b_body.dynamic_friction if b_body else 0
            mu = pow(aSF * aSF + bSF * bSF, 0.5)

            f = -f_vel / (a_inv_mass + b_inv_mass)

            if abs(f) < j * mu:
                friction = f * tangent
            else:
                mu = pow(aDF * aDF + bDF * bDF, 0.5)
                friction = -j * tangent * mu

            if a_body.is_simulated if a_body else False:
                a_body.velocity = a_vel - friction * a_inv_mass

            if b_body.is_simulated if b_body else False:
                b_body.velocity = b_vel - friction * b_inv_mass
