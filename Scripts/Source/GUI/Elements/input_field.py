import pygame as pg
import glm
import Scripts.Source.GUI.Elements.element as element_m
import Scripts.Source.GUI.Elements.block as block_m
import Scripts.Source.GUI.Elements.text as text_m


class InputField(element_m.Element):
    def __init__(self, name, rely_element, win_size: glm.vec2, gui,
                 color=(1, 1, 1, 1),
                 text_color=(0, 0, 0, 1),
                 text_size=1.5,
                 ):
        super().__init__(name, rely_element, win_size)

        self.color = glm.vec4(color)
        self.text_color = glm.vec4(text_color)
        self.text_size = text_size

        self.gui = gui

        self.background = block_m.Block(f"{name}_background", self, win_size, color)
        self.background.position.relative.right_top = glm.vec2(1)

        self.text = text_m.Text(f'{name}_text', self.background, win_size,
                                "WOW",
                                font_size=text_size,
                                color=text_color,
                                centered_y=True
                                )
        self.text.pivot = element_m.Pivot.LeftBottom
        self.text.render_letters_outside_boundaries = False
        self.text.moving_words_to_new_line = False
        self.text.position.evaluate_values_by_relative()

        self.default_time_between_delete_letter = 0.15
        self.accelerated_time = 0.05
        self._time_between_delete_letter = self.default_time_between_delete_letter
        self._last_delete_letter_time = 0
        self._timer_holding_backspace = 0
        self._backspace_was_released = True
        self.time_between_accelerating = 0.5
        self.editable = True

    def find_clicked_element(self, mouse_pos: glm.vec2):
        return self

    def update_position(self):
        super().update_position()

    def unselect(self):
        self.gui.active_input_field = None
        self.color += glm.vec4(0.1)
        self.background.color = self.color

    def handle_left_click(self, pos: glm.vec2):
        if self.editable:
            self.gui.active_input_field = self
            self.color -= glm.vec4(0.1)
            self.background.color = self.color
            return True
        return False

    def handle_keyboard_press(self, keys, pressed_char):
        if pressed_char:
            self.text.text += pressed_char
            self.update_position()
        elif keys[pg.K_RETURN]:
            self.gui.active_input_field = None
            self.color += glm.vec4(0.1)
        elif (keys[pg.K_BACKSPACE] and
              self.gui.app.time - self._last_delete_letter_time > self._time_between_delete_letter):
            self.text.text = self.text.text[:-1]
            self.update_position()

            self._backspace_was_released = False
            self._timer_holding_backspace += self.gui.app.delta_time / 50
            self._last_delete_letter_time = self.gui.app.time
            if (self._timer_holding_backspace >= self.time_between_accelerating and
                    self._time_between_delete_letter == self.default_time_between_delete_letter):
                self._time_between_delete_letter = self.accelerated_time
        if not keys[pg.K_BACKSPACE] and not self._backspace_was_released:
            self._time_between_delete_letter = self.default_time_between_delete_letter
            self._timer_holding_backspace = 0
            self._backspace_was_released = True

        return True

    def delete(self):
        self.gui = None
        self.background = None
        self.text = None
        super().delete()
