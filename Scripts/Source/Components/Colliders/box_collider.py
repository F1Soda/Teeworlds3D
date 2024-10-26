import Scripts.Source.Components.Colliders.collider as collider_m
import glm

NAME = 'Box Collider'
DESCRIPTION = 'Collider'


class BoxCollider(collider_m.Collider):
    def __init__(self):
        super().__init__(NAME, DESCRIPTION)
        self.min_point = glm.vec3(-0.5,-0.5,-0.5)
        