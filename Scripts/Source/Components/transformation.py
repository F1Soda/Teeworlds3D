import Scripts.Source.Components.component as component_m
import glm

NAME = "Transformation"
DESCRIPTION = "Описывает положение, вращение и масштобирование объекта"

VEC_UP = glm.vec3(0,1,0)

class Transformation(component_m.Component):
    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), moveable=True,
                 enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self._pos = glm.vec3(pos)
        self._rot = glm.vec3(rot)
        self._scale = glm.vec3(scale)

        self.m_model = glm.mat4()
        self.moveable = moveable

        self._forward = glm.vec3(1, 0, 0)
        self._up = glm.vec3(0, 1, 0)
        self._right = glm.vec3(0, 0, 1)

        self.children = []

        self.m_t = None
        self.m_tr = None
        self.m_r = None

    def add_child(self, child):
        self.children.append(child)
        self.update_model_matrix()

    @property
    def right(self):
        return self._right



    @property
    def forward(self):
        return self._forward


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
        self._pos = value
        self.update_model_matrix()
        for child in self.children:
            child.pos += diff

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

        x, y = glm.radians(self.rot.y), glm.radians(self.rot.x)

        self._forward.x = glm.cos(x) * glm.cos(y)
        self._forward.y = glm.sin(y)
        self._forward.z = glm.sin(x) * glm.cos(y)

        self._forward = glm.normalize(-self.forward)
        self._right = glm.normalize(glm.cross(VEC_UP, self.forward))
        self._up = glm.cross(self.forward, self.right)

        rot = glm.vec3([glm.radians(x) for x in diff])

        m_r = glm.rotate(glm.mat4(), rot.x, glm.vec3(1, 0, 0))
        m_r = glm.rotate(m_r, rot.y, glm.vec3(0, 1, 0))
        m_r = glm.rotate(m_r, rot.z, glm.vec3(0, 0, 1))

        for child in self.children:
            child.pos = m_r * child.pos
            if child.rely_object.name != "Game Camera":
                child.rot = (self._rot.x, self._rot.y, self._rot.z)


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
        self.m_model = self.m_t = glm.translate(glm.mat4(), self.pos)

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
