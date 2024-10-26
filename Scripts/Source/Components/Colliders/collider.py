import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.transformation as transformation_m
import Scripts.Source.Render.library as library_m
import glm
import moderngl as mgl


class Collider(component_m.Component):
    def __init__(self, name, description, enable=True):
        super().__init__(name, description, enable)
        self._transformation = None
        self._vertices = None
        self.rigidbody = None
        self.draw_collider = False
        self._vao_collider = None
        self._hidden_vbo = None
        self._center = glm.vec3()

        self._m_model = glm.mat4()

        self._hidden_line_shader = library_m.shader_programs['hidden_line']

        self.use_on_draw_gizmos = True

    @property
    def m_model(self):
        return None

    @property
    def vertices(self):
        return self._vertices

    @property
    def center(self):
        return self._center

    @property
    def hidden_vbo(self):
        return None

    def try_precalculate_collider(self):
        ...

    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def get_collide_point(self, collider):
        ...

    def find_furthest_point(self, direction) -> glm.vec3:
        max_point = glm.vec3()

        max_dot = -10e9
        for vertex in self.vertices:
            vertex = glm.mul(self.m_model, vertex)
            dot = glm.dot(vertex, direction)
            if dot > max_dot:
                max_dot = dot
                max_point = vertex

        return max_point

    def _init_vao_collider(self):
        self._hidden_line_shader['resolution'].write(glm.vec2(self.app.win_size))
        self._hidden_line_shader['dashSize'] = 10
        self._hidden_line_shader['gapSize'] = 10
        self._vao_collider = self.app.ctx.vertex_array(self._hidden_line_shader.bin_program,
                                                       [(self.hidden_vbo, '3f', 'in_position')])

    def on_gizmos(self, camera_component):
        self.use_on_draw_gizmos = True
        if self.draw_collider:
            if self._vao_collider is None:
                self._init_vao_collider()

            self._hidden_line_shader['m_model'].write(self.m_model)
            self._hidden_line_shader['m_view'].write(camera_component.m_view)
            self._hidden_line_shader['m_proj'].write(camera_component.m_proj)

            self.app.ctx.screen.color_mask = False, False, False, False
            self._vao_collider.render()
            self.app.ctx.line_width = 3.0
            # if self.level.render_hidden_lines == HiddenLineState.Both:
            #    self.app.ctx.depth_func = '1'
            # else:
            self.app.ctx.depth_func = '1'
            self.app.ctx.screen.depth_mask = False
            self.app.ctx.screen.color_mask = True, True, True, True
            self._vao_collider.render(mgl.LINES)

            self.app.ctx.screen.depth_mask = True
            self.app.ctx.depth_func = '<'

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        if self.rigidbody is None:
            self.rigidbody = self.rely_object.get_component_by_name("RigidBody")
        return self.rigidbody

    def delete(self):
        self._transformation = None
        self.rely_object = None

    def serialize(self) -> {}:
        return {
            'enable': self.enable
        }
