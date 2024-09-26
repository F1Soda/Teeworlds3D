import glm

import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.library as library_m
import Scripts.Source.General.Managers.data_manager as data_manager_m
import Scripts.Source.General.utils as utils_m

FONT_SIZE_SCALE = 0.01


class Text(element_m.Element):
    def __init__(self, name, rely_element, win_size: glm.vec2,
                 text,
                 font_size=1,
                 color=(1, 1, 1, 1),
                 space_between=0.1,
                 centered_x=False,
                 centered_y=False,
                 pivot=element_m.Pivot.LeftBottom,
                 ):
        super().__init__(name, rely_element, win_size)
        self._text = text
        self.font_size = font_size
        self.color = glm.vec4(color)
        self.space_between = space_between
        self.centered_x = centered_x
        self.centered_y = centered_y

        # Rendering
        self.vao = library_m.primitives_vao['text_quad']
        self.font_texture = library_m.textures['font']  # ['font_boundaries']
        self.shader_program = library_m.shader_programs['TextGUI']
        self.shader_program['letter_size'] = 16.0
        self.shader_program['color'].write(self.color)

        self.abs_quad_size = FONT_SIZE_SCALE * glm.vec2(font_size,
                                                        font_size * self.win_aspect_ratio) * self.win_size
        self.relative_win_quad_size = self.abs_quad_size / self.win_size

        # List with width for all letters
        self.letters_width = data_manager_m.DataManager.letters_width
        self.render_letters_outside_boundaries = True
        self.moving_words_to_new_line = False
        self.pivot = pivot
        self._text_to_print = self.text
        self._count_red_lines = 0
        # Properties
        self._relative_size = None

        # Custom m_gui for rendering quad by quad
        self.custom_m_gui = glm.mat4()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._text_to_print = value

    def process_window_resize(self, new_size: glm.vec2):
        self.abs_quad_size = self.abs_quad_size * new_size / self.win_size
        super().process_window_resize(new_size)
        # self.size = self.win_size * (self.relative_right_top - self.relative_left_bottom)

    def evaluate_text_size(self):
        size = glm.vec2(0, self.abs_quad_size.y)
        current_abs_right_pos = (self.rely_element.position.absolute.left_bottom.x +
                                 self.position.relative.left_bottom.x * self.rely_element.position.absolute.size.x)
        start_left_abs_pos = current_abs_right_pos
        left_abs_offset = current_abs_right_pos - self.rely_element.position.absolute.left_bottom.x
        max_right_abs_right_pos = 0
        self._count_red_lines = 0
        for i in range(len(self.text)):
            char = self.text[i]
            index = ord(char)
            y = index // 16
            x = index % 16
            letter_width = self.letters_width[y * 16 + x]
            current_abs_right_pos += self.abs_quad_size.x * (letter_width + self.space_between)
            if not self.render_letters_outside_boundaries:
                if current_abs_right_pos >= self.rely_element.position.absolute.right_top.x - left_abs_offset:
                    max_right_abs_right_pos = max(max_right_abs_right_pos, current_abs_right_pos)
                    current_abs_right_pos = start_left_abs_pos + self.abs_quad_size.x * (
                            letter_width + self.space_between)
                    if self.moving_words_to_new_line:
                        size.y += self.abs_quad_size.y
                        self._text_to_print = self._text_to_print[
                                              :i + self._count_red_lines] + "\n" + self._text_to_print[
                                                                                   i + self._count_red_lines:]
                        self._count_red_lines += 1
                    else:
                        self._text_to_print = self._text_to_print[:i]
        max_right_abs_right_pos = max(max_right_abs_right_pos, current_abs_right_pos)
        size.x = max_right_abs_right_pos - start_left_abs_pos
        if self.pivot == element_m.Pivot.LeftBottom:
            self.position.relative.right_top = (self.position.relative.left_bottom +
                                                size / self.rely_element.position.absolute.size)
        elif self.pivot == element_m.Pivot.Center:
            past_center = self.position.relative.copy.center
            self.position.relative.size = size / self.rely_element.position.absolute.size
            self.position.relative.center = past_center

    def update_position(self):
        self.evaluate_text_size()
        self.position.evaluate_values_by_relative()

        utils_m.copy_mat(self.position.m_gui, self.custom_m_gui)

        self.custom_m_gui[0][0] = self.relative_win_quad_size.x
        self.custom_m_gui[1][1] = self.relative_win_quad_size.y
        self.custom_m_gui[3][1] += self._count_red_lines * self.relative_win_quad_size.y

    def render(self):
        self.shader_program['color'] = self.color
        self.shader_program['texture_0'] = 0
        self.font_texture.use()

        m_gui_c3_r0 = self.custom_m_gui[3][0]
        m_gui_c3_r1 = self.custom_m_gui[3][1]

        current_right_relative_corner = self.position.relative.left_bottom.x

        for char in self._text_to_print:

            if char == "\n":
                self.custom_m_gui[3][0] = m_gui_c3_r0
                self.custom_m_gui[3][1] -= self.relative_win_quad_size.y
                continue

            index = ord(char)
            y = index // 16
            x = index % 16

            # Offset In Texture
            offset = glm.vec2(x * 1 / 16, (31 - y) * 1 / 16)
            self.shader_program['offset'].write(offset)

            # M_GUI
            self.shader_program['m_gui'].write(self.custom_m_gui)

            self.vao.render()

            # Shift Quad
            letter_width = self.letters_width[y * 16 + x]
            self.custom_m_gui[3][0] += self.relative_win_quad_size.x * (letter_width + self.space_between)
            current_right_relative_corner += self.position.relative.size.x / len(self._text_to_print)

        self.custom_m_gui[3][0] = m_gui_c3_r0
        self.custom_m_gui[3][1] = m_gui_c3_r1

    @staticmethod
    def precalculate_block_height(text, text_size):
        pass

    def delete(self):
        self.vao = None
        self.shader_program = None
        self.font_texture = None
        super().delete()
