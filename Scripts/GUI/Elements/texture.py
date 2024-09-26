import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.library as library_m
import glm
import moderngl as mgl


class Texture(element_m.Element):
    def __init__(self, name, rely_element, win_size, texture, is_depth_texture=False):
        super().__init__(name, rely_element, win_size)
        self.vao = library_m.primitives_vao['textured_quad']  # type: mgl.VertexArray
        self.shader_program = library_m.shader_programs['TextureGUI']
        self.texture = texture
        self.is_depht_texture = is_depth_texture

    def render(self):
        self.shader_program['m_gui'].write(self.position.m_gui)
        self.shader_program['texture0'] = 0
        self.shader_program['depthTexture'] = self.is_depht_texture
        self.texture.use()
        self.vao.render()
        super().render()

    def handle_right_hold(self, pos: glm.vec2):
        return True

    def delete(self):
        self.vao = None
        self.shader_program = None
        self.texture = None
        super().delete()
