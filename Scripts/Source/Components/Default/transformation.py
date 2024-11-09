import Scripts.Source.Components.Default.component as component_m
import glm
import math

NAME = "Transformation"
DESCRIPTION = "Описывает положение, вращение и масштобирование объекта"

VEC_UP = glm.vec3(0, 1, 0)


class Transformation(component_m.Component):
    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), moveable=True,
                 enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self._pos = glm.vec3(pos)
        self._rot = glm.vec3(rot)
        self._scale = glm.vec3(scale)

        self._global_pos = glm.vec3(pos)
        # self._rot = glm.vec3(rot)
        # self._scale = glm.vec3(scale)

        self.m_model = glm.mat4()
        self.moveable = moveable

        self._forward = glm.vec3(0, 0, 1)
        self._up = glm.vec3(0, 1, 0)
        self._right = glm.vec3(1, 0, 0)

        self.children = []

        self.parent = None

        self.m_t = None
        self.m_tr = None
        self.m_r = None

    def recalculate_local_pos(self, parent_global_pos):
        self._pos -= parent_global_pos

    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        self.update_model_matrix()
        child.recalculate_local_pos(self._global_pos)

    @property
    def right(self):
        return self._right

    @property
    def forward(self):
        return self._forward

    @forward.setter
    def forward(self, value):
        # Convert input to glm.vec3 if it’s a tuple
        if isinstance(value, tuple):
            value = glm.vec3(*value)

        # Update the forward vector
        self._forward = glm.normalize(value)  # Normalize to avoid scaling issues

        # Calculate the new rotation matrix using glm.lookAt
        self.m_r = glm.lookAt(self.pos, self.pos + self._forward, VEC_UP)

        # Extract Euler angles from the rotation matrix
        self._rot = -glm.degrees(glm.eulerAngles(glm.quat_cast(self.m_r)))


        # Call update_model_matrix to update the model matrix with the new rotation
        self.update_model_matrix()



    @property
    def up(self):
        return self._up

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        if isinstance(value, tuple):
            value = glm.vec3(*value)
        diff = value - self._pos
        self._global_pos += diff
        self._pos = value
        self.update_model_matrix()
        for child in self.children:
            child.global_pos = child.global_pos + diff

    @property
    def global_pos(self):
        return self._global_pos

    @global_pos.setter
    def global_pos(self, value):
        if isinstance(value, tuple):
            value = glm.vec3(*value)
        diff = value - self._pos
        self._global_pos = value
        self.update_model_matrix()


    @property
    def rot(self):
        return self._rot

    @rot.setter
    def rot(self, value):
        if isinstance(value, tuple):
            value = glm.vec3(*value)
        diff = value - self._rot
        self._rot = value

        self.update_model_matrix()

        self._forward.x = -self.m_r[0][2]
        self._forward.y = self.m_r[1][2]
        self._forward.z = self.m_r[2][2]

        self._right.x = -self.m_r[0][0]
        self._right.y = self.m_r[1][0]
        self._right.z = self.m_r[2][0]

        self._up.x = -self.m_r[0][1]
        self._up.y = self.m_r[1][1]
        self._up.z = self.m_r[2][1]

        rot = glm.vec3([glm.radians(x) for x in diff])

        m_r = glm.rotate(glm.mat4(), rot.x, glm.vec3(1, 0, 0))
        m_r = glm.rotate(m_r, rot.y, glm.vec3(0, 1, 0))
        m_r = glm.rotate(m_r, rot.z, glm.vec3(0, 0, 1))

        for child in self.children:
            child.pos = m_r * child.pos
            child.rot = self._rot
        # child.pos = child.pos
        # child.pos.x = child.pos.x * glm.cos(rot.y)
        # child.pos.y = child.pos.y * glm.sin(rot.x)
        # if child.rely_object.name != "Game Camera":

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if isinstance(value, glm.vec3):
            self._scale = value
        elif isinstance(value, tuple):
            self._scale = glm.vec3(*value)
        self.update_model_matrix()

    def update_model_matrix(self):
        rot = glm.vec3([glm.radians(x) for x in self.rot])

        # position
        self.m_model = self.m_t = glm.translate(glm.mat4(), self.global_pos)

        # rotation
        self.m_r = glm.rotate(glm.mat4(), rot.x, glm.vec3(1, 0, 0))
        self.m_r = glm.rotate(self.m_r, rot.y, glm.vec3(0, 1, 0))
        self.m_r = glm.rotate(self.m_r, rot.z, glm.vec3(0, 0, 1))
        self.m_model = self.m_tr = self.m_t * self.m_r

        # scale
        self.m_model = glm.scale(self.m_model, self._scale)

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self.update_model_matrix()

    def on_change(self):
        self.update_model_matrix()

    def serialize(self) -> {}:
        return {
            'pos': ('vec', self.pos.to_tuple()),
            'rot': ('vec', self.rot.to_tuple()),
            'scale': ('vec', self.scale.to_tuple()),
            'moveable': self.moveable,
            'enable': self.enable
        }
