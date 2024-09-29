import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.transformation as transformation_m
import glm

NAME = "Camera"
DESCRIPTION = "Компонент камеры для отрисовки"


class Camera(component_m.Component):
    def __init__(self, near=0.1, far=1000, fov=50, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        # right-handed system

        self.fov = fov
        self.near = near
        self.far = far

        # Matrix
        self.m_ortho = None
        self.m_proj = None
        self.m_view = glm.mat4()

        self._transformation = None
        self.aspect_ratio = None
        self.top_bound = None
        self.right_bound = None

    def process_window_resize(self, new_size):
        self.aspect_ratio = new_size[0] / new_size[1]
        self.m_proj = self.get_projection_matrix()
        self.right_bound = self.aspect_ratio * self.top_bound
        self.m_ortho = self.get_orthographic_matrix()

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self.aspect_ratio = app.win_size[0] / app.win_size[1]
        self._transformation = self.rely_object.get_component_by_name(
            'Transformation')  # type: transformation_m.Transformation

        self.top_bound = self.near * glm.tan(glm.radians(self.fov / 2))
        self.right_bound = self.aspect_ratio * self.top_bound

        self.get_view_matrix(self.m_view)
        self.m_proj = self.get_projection_matrix()
        self.m_ortho = self.get_orthographic_matrix()

    def apply(self):
        self.get_view_matrix(self.m_view)

    def get_view_matrix(self, out_mat):
        out_mat[0][0] = self.transformation.right.x
        out_mat[1][0] = self.transformation.right.y
        out_mat[2][0] = self.transformation.right.z
        out_mat[3][0] = -glm.dot(self.transformation.pos, self.transformation.right)

        out_mat[0][1] = self.transformation.up.x
        out_mat[1][1] = self.transformation.up.y
        out_mat[2][1] = self.transformation.up.z
        out_mat[3][1] = -glm.dot(self.transformation.pos, self.transformation.up)

        out_mat[0][2] = self.transformation.forward.x
        out_mat[1][2] = self.transformation.forward.y
        out_mat[2][2] = self.transformation.forward.z
        out_mat[3][2] = -glm.dot(self.transformation.pos, self.transformation.forward)

    def get_projection_matrix(self) -> glm.mat4x4:
        return glm.perspective(glm.radians(self.fov), self.aspect_ratio, self.near, self.far)

    def get_orthographic_matrix(self):
        return glm.ortho(-self.right_bound, self.right_bound, -self.top_bound, self.top_bound, self.near, self.far)

    @property
    def transformation(self) -> transformation_m.Transformation:
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_name('Transformation')
        return self._transformation

    @transformation.setter
    def transformation(self, value: transformation_m.Transformation):
        self._transformation = value

    def delete(self):
        self._transformation = None
        self.rely_object = None
        self.app = None

    def serialize(self) -> {}:
        return {
            'near': self.near,
            'far': self.far,
            'fov': self.fov,
            'enable': self.enable
        }
