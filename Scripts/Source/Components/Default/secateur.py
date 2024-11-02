import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Render.library as library_m
import moderngl as mgl

NAME = "Secateur"
DESCRIPTION = "Objects with component section will be rendering only inside object mesh"


class Secateur(component_m.Component):
    # External initialization
    background_stencil_texture = None
    front_stencil_texture = None
    background_stencil_fbo = None
    front_stencil_fbo = None

    @staticmethod
    def clear_context(ctx):
        Secateur.background_stencil_fbo.use()
        ctx.clear()
        Secateur.front_stencil_fbo.use()
        ctx.clear()

    @staticmethod
    def init_buffers(app):
        size = (int(app.win_size.x), int(app.win_size.y))
        Secateur.background_stencil_texture = app.ctx.texture(size, 1, dtype='f1')
        Secateur.background_stencil_texture.repeat_x = False
        Secateur.background_stencil_texture.repeat_y = False
        Secateur.background_stencil_texture.filter = (mgl.NEAREST, mgl.NEAREST)
        Secateur.background_stencil_texture.swizzle = 'RRR1'

        Secateur.front_stencil_texture = app.ctx.texture(size, 1, dtype='f1')
        Secateur.front_stencil_texture.repeat_x = False
        Secateur.front_stencil_texture.repeat_y = False
        Secateur.front_stencil_texture.filter = (mgl.NEAREST, mgl.NEAREST)
        Secateur.front_stencil_texture.swizzle = 'RRR1'

        Secateur.background_stencil_fbo = app.ctx.framebuffer(
            color_attachments=[Secateur.background_stencil_texture],
            depth_attachment=app.ctx.depth_texture(size)
        )

        Secateur.front_stencil_fbo = app.ctx.framebuffer(
            color_attachments=[Secateur.front_stencil_texture],
            depth_attachment=app.ctx.depth_texture(size)
        )

    @staticmethod
    def delete_buffers():
        # Background Stencil
        Secateur.background_stencil_texture.release()
        Secateur.background_stencil_fbo.color_attachments[0].release()
        Secateur.background_stencil_fbo.depth_attachment.release()
        Secateur.background_stencil_fbo.release()

        # Front Stencil
        Secateur.front_stencil_texture.release()
        Secateur.front_stencil_fbo.color_attachments[0].release()
        Secateur.front_stencil_fbo.depth_attachment.release()
        Secateur.front_stencil_fbo.release()

    def __init__(self, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self.shader = library_m.shader_programs['silhouette']

        self.renderer = None
        self._vao = None

    def init(self, app, rely_object):
        super().init(app, rely_object)

        self.renderer = self.rely_object.get_component_by_name("Renderer")
        if self.renderer:
            self._vao = self.renderer.get_vao(self.shader, self.renderer.mesh)
        self.shader['m_proj'].write(self.app.level.camera_component.m_proj)
        # frame_debugger_m.FrameDebugger.draw_texture(self.background_stencil_texture, glm.vec2(0.85))
        # frame_debugger_m.FrameDebugger.draw_texture(self.front_stencil_texture, glm.vec2(0.85, 0.55))

    def process_window_resize(self, new_size):
        self.shader['m_proj'].write(self.app.level.camera_component.m_proj)

    def apply(self):
        pass
        # if self._vao is None:
        #     return
        # self.shader['m_view'].write(self.app.level.camera_component.m_view)
        # self.shader['m_model'].write(self.rely_object.transformation.m_model)
        # self.shader['subtract'] = False
        #
        # # Background Stencil
        # self.background_stencil_fbo.use()
        # # self.app.ctx.clear()
        # self.app.ctx.cull_face = 'front'
        # self._vao.render()
        #
        # # Front Stencil
        # self.front_stencil_fbo.use()
        # # self.app.ctx.clear()
        # self.app.ctx.cull_face = 'back'
        # self._vao.render()
        #
        # self.app.ctx.screen.use()

    def serialize(self) -> {}:
        return {
            'enable': self.enable
        }

    def delete(self):
        self.renderer = None
        self._vao.release()
        self._vao = None
        super().delete()
