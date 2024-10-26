import Scripts.Source.Components.component as component_m
import Scripts.Source.Render.library as library_m
import Scripts.Source.Components.secateur as secateur_m
import Scripts.Source.Components.plane as plane_m
import moderngl as mgl

NAME = "Section"
DESCRIPTION = "Add this component to make section with objects with Secateur component"


class Section(component_m.Component):
    def __init__(self, inverse=False, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        self.plane = None
        self._vao = None
        self._subtract_vao = None

        self.inverse = inverse

        self._material = library_m.materials['section']
        self._section_shader = library_m.shader_programs['section']

        self._subtract_shader = library_m.shader_programs['silhouette']

    def init(self, app, rely_object):
        super().init(app, rely_object)

        self.plane = self.rely_object.get_component_by_name("Plane")
        if self.plane:
            self._vao = self.plane.get_vao(self._material.shader_program)
            if self.plane in self.app.level.transparency_renderer:
                self.app.level.transparency_renderer.remove_object(self.plane)
                self.app.level.opaque_renderer.append(self.plane)
            self._subtract_vao = self.plane.get_vao(self._subtract_shader)

        # Material Initialization
        self._material.camera_component = self.app.level.camera_component
        self._material.camera_transformation = self.app.level.camera.transformation
        self._material.initialize()

        # Setting Default Values
        self._material['texture_0'].value = secateur_m.Secateur.background_stencil_texture
        self._material['texture_1'].value = secateur_m.Secateur.front_stencil_texture
        self._subtract_shader['m_proj'].write(self.app.level.camera_component.m_proj)
        self._material['inverse'].value = self.inverse
        # Change Default Apply Method
        self.plane.apply = self.renderer_apply

        # if self.inverse:
        #    self.app.scene.transparency_renderer.remove(self.plane)
        #   self.app.scene.opaque_renderer.append(self.plane)

    def process_window_resize(self, new_win_size):
        self._material.update_projection_matrix(self.app.level.camera_component.m_proj)
        self._material['winSize'] = new_win_size
        self._material['texture_0'].value = secateur_m.Secateur.background_stencil_texture
        self._material['texture_1'].value = secateur_m.Secateur.front_stencil_texture

        self._subtract_shader['m_proj'].write(self.app.level.camera_component.m_proj)

    def renderer_apply(self):
        # Update Model Matrix For Plane
        self.plane.update_m_model()

        if self._vao is None or secateur_m.Secateur.background_stencil_texture is None:
            return

        self._material.update(self.rely_object.transformation, self.app.level.light)
        self._material['inverse'].value = self.inverse
        self._section_shader['inverse'] = self.inverse

        self._subtract_shader['m_view'].write(self.app.level.camera_component.m_view)
        self._subtract_shader['m_model'].write(self.rely_object.transformation.m_model)
        self._subtract_shader['subtract'] = True

        # Subtract Plane Silhouette From Background
        secateur_m.Secateur.background_stencil_fbo.use()
        self._subtract_vao.render()

        # Subtract Plane Silhouette From Front
        secateur_m.Secateur.front_stencil_fbo.use()
        self._subtract_vao.render()

        # Usual Drawing
        self.app.ctx.screen.use()
        # Behaviour can be different
        self._vao.render()

    def serialize(self) -> {}:
        return {
            'inverse': self.inverse,
            'enable': self.enable
        }

    def delete(self):
        self.plane.apply = plane_m.Plane.apply
        self.plane = None
        self._material = None
        self._vao.release()
        self._vao = None
        super().delete()
