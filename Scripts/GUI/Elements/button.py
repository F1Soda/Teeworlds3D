import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.Elements.text as text_m
import Scripts.GUI.Elements.block as block_m
import glm


class Button(element_m.Element):
    def __init__(self, name, rely_element, win_size: glm.vec2, gui,
                 text,
                 text_size,
                 action,
                 color=(1, 1, 1, 1),
                 text_color=(0, 0, 0, 1),
                 value=None
                 ):
        super().__init__(name, rely_element, win_size)

        self.gui = gui
        self._button_text = text
        self._color = color
        self.text_color = text_color
        self.text_size = text_size
        self.action = action

        self.text = None
        self.background = None

        self.value = value

        self.init_button()

    def init_button(self):
        self.background = block_m.Block(f"{self.name}_background", self, self.win_size, self.color)

        self.background.position.relative.right_top = glm.vec2(1)
        self.background.position.evaluate_values_by_relative()
        self.text = text_m.Text(f"{self.name}_text", self.background, self.win_size,
                                self._button_text,
                                centered_x=True,
                                centered_y=True,
                                font_size=self.text_size,
                                space_between=0.1,
                                pivot=element_m.Pivot.Center,
                                color=self.text_color
                                )
        self.text.position.relative.center = glm.vec2(0.5, 0.5)
        self.text.position.evaluate_values_by_relative()

    def render(self):
        self.background.render()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.background.color = value

    @property
    def button_text(self):
        return self._button_text

    @button_text.setter
    def button_text(self, value):
        self._button_text = value
        self.text.text = value

    def find_clicked_element(self, mouse_pos: glm.vec2):
        return self

    def handle_left_click(self, pos: glm.vec2):
        if self.action:
            self.action(self, self.gui, pos)

    def delete(self):
        self.gui = None
        self.action = None
        self.text = None
        self.background = None
        self.value = None
        super().delete()
