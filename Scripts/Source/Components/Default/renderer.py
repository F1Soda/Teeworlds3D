import Scripts.Source.Components.Default.component as component_m
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
    def __init__(self, material: material_m.Material, enable_hidden_line=False, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        # Settings
        self.default_line_width = 3.0
        self.default_point_size = 4.0
        self._init_hidden_line_vao = enable_hidden_line
        self.hidden_line_shader = library_m.shader_programs['hidden_line']

        # Other

        self._material = material
        self.picking_material = library_m.materials['object_picking']

        self._mesh_filter = None
        self.level = None
        self.camera_transform = None
        self.camera_component = None
        self.transformation = None
        self.ctx = None
        self._vao = None
        self._vao_picking = None
        self.vao_hidden_line = None

    @property
    def mesh_filter(self):
        if self._mesh_filter is None:
            self._mesh_filter = self.rely_object.get_component_by_name("Mesh Filter")
        return self._mesh_filter

    @mesh_filter.setter
    def mesh_filter(self, value):
        self._mesh_filter = value
        self._vao = self.get_vao(self.material.shader_program, self.mesh_filter)
        self._vao_picking = self.get_vao(self.picking_material.shader_program, self.mesh_filter.mesh)

    def _enable_hidden_line(self):
        if self.mesh_filter is None:
            return
        self.hidden_line_shader['resolution'].write(glm.vec2(self.app.win_size))
        self.hidden_line_shader['dashSize'] = 10
        self.hidden_line_shader['gapSize'] = 10
        self.vao_hidden_line = self.ctx.vertex_array(self.hidden_line_shader.bin_program,
                                                     [(self.mesh_filter.mesh.hidden_vbo, '3f', 'in_position')])

    def init(self, app, rely_object):
        super().init(app, rely_object)
        # Scene
        self.level = self.rely_object.level  # type: level_m.Level

        self.ctx = app.ctx  # type: mgl.Context

        # Camera
        self.camera_transform = self.level.camera.transformation
        self.camera_component = self.level.camera.get_component_by_name('Camera')

        self.picking_material.camera_component = self.camera_component
        self.picking_material.camera_transformation = self.camera_component.transformation
        self.transformation = self.rely_object.transformation
        self.picking_material.initialize()

        self.material.camera_component = self.camera_component
        self.material.camera_transformation = self.camera_component.transformation
        self.material.light_component = self.light_component
        self.material.initialize()

        self._vao = self.get_vao(self.material.shader_program, self.mesh_filter)
        self._vao_picking = self.get_vao(self.picking_material.shader_program, self.mesh_filter)

        if self._init_hidden_line_vao:
            self._enable_hidden_line()

    def update_render_mode(self):
        # Вот тут я хз че за блять remove_object, когда transparency_renderer это list. Пускай останется =)
        if self.material.render_mode == material_m.RenderMode.Opaque:
            if self in self.level.transparency_renderer:
                self.level.transparency_renderer.remove_object(self)
            if self not in self.level.opaque_renderer:
                self.level.opaque_renderer.append(self)
        else:
            if self in self.level.opaque_renderer:
                self.level.opaque_renderer.remove_object(self)
            if self not in self.level.transparency_renderer:
                self.level.transparency_renderer.append(self)

    @property
    def vao(self):
        if self._vao is None:
            self._vao = self.get_vao(self._material.shader_program, self.mesh_filter)
        return self._vao

    @vao.setter
    def vao(self, value):
        self._vao = value

    @property
    def vao_picking(self):
        if self._vao_picking is None:
            self._vao_picking = self.get_vao(self.picking_material.shader_program, self.mesh_filter)
        return self._vao_picking

    @vao_picking.setter
    def vao_picking(self, value):
        self._vao_picking = value

    @property
    def light_component(self):
        return self.level.light

    def update_projection_matrix(self, m_proj):
        self.material.update_projection_matrix(m_proj)
        self.picking_material.update_projection_matrix(m_proj)

    def get_vao(self, shader_program, mesh_filter) -> mgl.VertexArray | None:
        if shader_program is None or mesh_filter is None:
            return None
        vao = self.ctx.vertex_array(shader_program.bin_program, [
            (mesh_filter.mesh.vbo, mesh_filter.mesh.data_format, *mesh_filter.mesh.attributes)])
        return vao

    def process_window_resize(self, new_size):
        self.update_projection_matrix(self.camera_component.m_proj)
        self.hidden_line_shader['resolution'].write(glm.vec2(self.app.win_size))

    def apply(self):
        if self.vao is None:
            return
        self.material.update(self.transformation, self.light_component)

        if self.material.render_mode == material_m.RenderMode.Opaque:
            if self.level.render_hidden_lines != HiddenLineState.Off and self.vao_hidden_line:

                self.hidden_line_shader['m_model'].write(self.transformation.m_model)
                self.hidden_line_shader['m_view'].write(self.camera_component.m_view)
                self.hidden_line_shader['m_proj'].write(self.camera_component.m_proj)

                self.hidden_line_shader[
                    'dashed'] = True if self.level.render_hidden_lines == HiddenLineState.Dash else False
                self.ctx.screen.color_mask = False, False, False, False
                self.vao.render()
                self.ctx.line_width = 3.0
                if self.level.render_hidden_lines == HiddenLineState.Both:
                    self.ctx.depth_func = '1'
                else:
                    self.ctx.depth_func = '>'
                self.ctx.screen.depth_mask = False
                self.ctx.screen.color_mask = True, True, True, True
                self.vao_hidden_line.render(mgl.LINES)

                self.ctx.screen.depth_mask = True
                self.ctx.depth_func = '<'
            else:
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
        self.vao = self.get_vao(self._material.shader_program, self.mesh_filter)

    def delete(self):
        if self.level is None:
            pass
        if self in self.level.transparency_renderer:
            self.level.transparency_renderer.remove(self)
        elif self in self.level.opaque_renderer:
            self.level.opaque_renderer.remove(self)

        self.rely_object = None
        self.transformation = None
        self.camera_component = None
        self.camera_transform = None
        self.level = None
        self.ctx = None
        self.vao = None
        if self.vao_hidden_line:
            self.vao_hidden_line.release()
        self.vao_hidden_line = None
        self._material = None
        self.mesh_filter.delete()
        self._mesh_filter = None

    def serialize(self) -> {}:
        return {
            'material': self.material.name,
            'enable': self.enable,
            'enable_hidden_line': self._init_hidden_line_vao
        }
