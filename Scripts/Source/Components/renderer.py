import Scripts.Source.Components.component as component_m
import Scripts.Source.General.Game.level as scene_m
import Scripts.Source.Render.mesh as mesh_m
import Scripts.Source.Render.material as material_m
import Scripts.Source.Render.library as library_m
import glm
import moderngl as mgl
import enum

NAME = 'Renderer'
DESCRIPTION = 'Отвечает за отрисовку'


class HiddenLineState(enum.Enum):
    Off = 0,
    Line = 1,
    Dash = 2,
    Both = 3


class Renderer(component_m.Component):

    def __init__(self, mesh: mesh_m.Mesh, material: material_m.Material, enable_hidden_line=False, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        # Settings
        self.default_line_width = 3.0
        self.default_point_size = 4.0
        self._init_hidden_line_vao = enable_hidden_line
        self.hidden_line_shader = library_m.shader_programs['hidden_line']

        # Other
        self.mesh = mesh
        self._material = material
        self.picking_material = library_m.materials['object_picking']

        self.scene = None
        self.camera_transform = None
        self.camera_component = None
        self.transformation = None
        self.ctx = None
        self.vao = None
        self.vao_picking = None
        self.vao_hidden_line = None

    def _enable_hidden_line(self):
        self.hidden_line_shader['resolution'].write(glm.vec2(self.app.win_size))
        self.hidden_line_shader['dashSize'] = 10
        self.hidden_line_shader['gapSize'] = 10
        self.vao_hidden_line = self.ctx.vertex_array(self.hidden_line_shader.bin_program,
                                                     [(self.mesh.hidden_vbo, '3f', 'in_position')])

    def init(self, app, rely_object):
        super().init(app, rely_object)
        # Scene
        self.scene = self.rely_object.level  # type: scene_m.Level

        self.ctx = app.ctx  # type: mgl.Context

        # Camera
        self.camera_transform = self.scene.camera.transformation
        self.camera_component = self.scene.camera.get_component_by_name('Camera')

        self.picking_material.camera_component = self.camera_component
        self.picking_material.camera_transformation = self.camera_component.transformation
        self.transformation = self.rely_object.transformation
        self.picking_material.initialize()

        self.material.camera_component = self.camera_component
        self.material.camera_transformation = self.camera_component.transformation
        self.material.light_component = self.light_component
        self.material.initialize()

        self.vao = self.get_vao(self._material.shader_program, self.mesh)
        self.vao_picking = self.get_vao(self.picking_material.shader_program, self.mesh)

        if self._init_hidden_line_vao:
            self._enable_hidden_line()

    def update_render_mode(self):
        if self.material.render_mode == material_m.RenderMode.Opaque:
            if self in self.scene.transparency_renderer:
                self.scene.transparency_renderer.remove(self)
            if self not in self.scene.opaque_renderer:
                self.scene.opaque_renderer.append(self)
        else:
            if self in self.scene.opaque_renderer:
                self.scene.opaque_renderer.remove(self)
            if self not in self.scene.transparency_renderer:
                self.scene.transparency_renderer.append(self)

    @property
    def light_component(self):
        return self.scene.light

    def update_projection_matrix(self, m_proj):
        self.material.update_projection_matrix(m_proj)
        self.picking_material.update_projection_matrix(m_proj)

    def get_model_matrix(self) -> glm.mat4x4:
        return glm.mat4() if self.transformation is None else self.transformation.m_model

    def get_vao(self, shader_program, mesh) -> mgl.VertexArray:
        vao = self.ctx.vertex_array(shader_program.bin_program, [(mesh.vbo, mesh.data_format, *mesh.attributes)])
        return vao

    def process_window_resize(self, new_size):
        self.update_projection_matrix(self.camera_component.m_proj)
        self.hidden_line_shader['resolution'].write(glm.vec2(self.app.win_size))

    def apply(self):
        self.material.update(self.transformation, self.light_component)
        self.hidden_line_shader['m_model'].write(self.transformation.m_model)
        self.hidden_line_shader['m_view'].write(self.camera_component.m_view)
        self.hidden_line_shader['m_proj'].write(self.camera_component.m_proj)

        if self.material.render_mode == material_m.RenderMode.Opaque:
            if self.scene.render_hidden_lines != HiddenLineState.Off and self.vao_hidden_line:
                self.hidden_line_shader[
                    'dashed'] = True if self.scene.render_hidden_lines == HiddenLineState.Dash else False
                self.ctx.screen.color_mask = False, False, False, False
                self.vao.render()
                self.ctx.line_width = 3.0
                if self.scene.render_hidden_lines == HiddenLineState.Both:
                    self.ctx.depth_func = '1'
                else:
                    self.ctx.depth_func = '>'
                self.ctx.screen.depth_mask = False
                self.ctx.screen.color_mask = True, True, True, True
                self.vao_hidden_line.render(mgl.LINES)

                self.ctx.screen.depth_mask = True
                self.ctx.depth_func = '<'
            self.vao.render()
        elif self.material.render_mode == material_m.RenderMode.Transparency:
            self.ctx.enable(mgl.BLEND)
            self.vao.render()
            self.ctx.disable(mgl.BLEND)

    def render_picking_material(self):
        self.picking_material.update(self.transformation, None)
        self.vao_picking.render()

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        self._material = value
        self.vao.release()
        self.vao = self.get_vao(self._material.shader_program, self.mesh)

    def delete(self):
        self.rely_object = None
        self.transformation = None
        self.camera_component = None
        self.camera_transform = None
        self.scene = None
        self.ctx = None
        self.vao = None
        if self.vao_hidden_line:
            self.vao_hidden_line.release()
        self.vao_hidden_line = None
        self._material = None
        self.mesh = None

    def serialize(self) -> {}:
        return {
            'mesh': self.mesh.name,
            'material': self.material.name,
            'enable': self.enable,
            'enable_hidden_line': self._init_hidden_line_vao
        }
