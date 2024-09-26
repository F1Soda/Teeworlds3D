import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.library as library_m
import glm
import moderngl as mgl


class Block(element_m.Element):
    def __init__(self, name, rely_element, win_size, color=(0, 0, 0, 0)):
        super().__init__(name, rely_element, win_size)
        self.vao = library_m.primitives_vao['quad']  # type: mgl.VertexArray
        self.shader_program = library_m.shader_programs['BlockGUI']
        self.color = glm.vec4(color)

    def render(self):
        # rely_element = self.rely_element if self.rely_element is not None else self
        self.shader_program['color'].write(self.color)
        self.shader_program['m_gui'].write(self.position.m_gui)
        self.vao.render()
        super().render()

    def handle_right_hold(self, pos: glm.vec2):
        return True

    def delete(self):
        self.vao = None
        self.shader_program = None
        super().delete()
