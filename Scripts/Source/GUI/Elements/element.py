import glm
import enum
import Scripts.Source.GUI.position as position_m


class Pivot(enum.Enum):
    Center = 0,
    LeftBottom = 1
    LeftTop = 2
    RightTop = 3
    RightBottom = 4
    Left = 5
    Top = 6
    Right = 7
    Bottom = 8


class Element:

    def __init__(self, name, rely_element, win_size: glm.vec2):
        self.name = name
        self.win_size = win_size
        self.rely_element = rely_element
        self.elements = []
        self.recalculate_size_by = Pivot.LeftBottom

        self.pivot = Pivot.Center

        self.position = position_m.Position(self.win_size)
        self.active = True

        if self.rely_element:
            self.rely_element.elements.append(self)
            self.position.rely_element_position = self.rely_element.position

    @property
    def win_aspect_ratio(self):
        return self.win_size.x / self.win_size.y

    def process_window_resize(self, new_size: glm.vec2):
        self.win_size = new_size
        self.position.recalculate(self.win_size)
        for element in self.elements:
            element.process_window_resize(new_size)

    def update_position(self):
        self.position.evaluate_values_by_relative()
        for element in self.elements:
            element.update_position()

    def add(self, element):
        self.elements.append(element)

    def render(self):
        for element in self.elements:
            if element.active:
                element.render()

    def delete(self):
        self.position.rely_element_position = None
        self.position = None
        for element in self.elements:
            element.delete()
        self.rely_element = None
        self.elements.clear()

    def find_clicked_element(self, mouse_pos: glm.vec2):
        for element in self.elements:
            if element.active and element.position.check_if_clicked(mouse_pos):
                return element.find_clicked_element(mouse_pos)
        return self

    def handle_left_click(self, pos: glm.vec2):
        ...

    def handle_left_release(self, pos: glm.vec2):
        ...

    def handle_left_hold(self, pos: glm.vec2):
        ...

    def handle_right_click(self, pos: glm.vec2):
        ...

    def handle_right_hold(self, pos: glm.vec2):
        ...

    def handle_right_release(self, pos: glm.vec2):
        ...

    def handle_keyboard_press(self, keys, pressed_char):
        ...

    def __str__(self):
        return f"GUI. Name: {self.name}, Type: {self.__class__.__name__}"

    def __repr__(self):
        return str(self)
