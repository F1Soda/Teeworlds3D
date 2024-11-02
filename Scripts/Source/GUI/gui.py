import glm
import Scripts.Source.GUI.Elements.elements as elements_m


class GUI:
    def __init__(self, app, win_size):
        self.app = app
        self.win_size = glm.vec2(win_size)
        self.aspect_ratio = win_size[0] / win_size[1]

        self.canvas = elements_m.Block("Canvas", None, self.win_size)
        self.canvas.position.relative_window.right_top = glm.vec2(1)
        self.canvas.position.relative.right_top = glm.vec2(1)
        self.canvas.position.evaluate_values_by_relative_window()

        self.last_clicked_element = None
        self.active_sub_menu = None
        self.active_input_field = None
        self.windows = []

    def process_window_resize(self, new_size: glm.vec2):
        self.win_size = new_size
        self.canvas.process_window_resize(new_size)

    def render(self):
        self.canvas.render()
        for window in self.windows:
            window.render()

    def clear(self):
        for element in self.canvas.elements:
            element.delete()

    def find_clicked_element(self, mouse_pos: glm.vec2):
        if self.active_sub_menu and self.active_sub_menu.position.check_if_clicked(mouse_pos):
            return self.active_sub_menu.find_clicked_element(mouse_pos)
        return self.canvas.find_clicked_element(mouse_pos)

    def handle_left_click(self, mouse_pos: glm.vec2):
        for window in self.windows[::-1]:
            element = window.find_clicked_element(mouse_pos)
            if element:
                if self.active_input_field:
                    if element.name == self.active_input_field.name:
                        return
                    else:
                        self.active_input_field.unselect()
                self.last_clicked_element = element
                element.handle_left_click(mouse_pos)
                return

        element = self.find_clicked_element(mouse_pos)
        if self.active_sub_menu:
            self.active_sub_menu.active = False
            self.active_sub_menu = None
        if self.active_input_field:
            if element.name == self.active_input_field.name:
                return
            else:
                self.active_input_field.unselect()
        if element.name == "Canvas":
            self.last_clicked_element = None
            return False
        else:
            element.handle_left_click(mouse_pos)
            self.last_clicked_element = element
            return True

    def handle_left_hold(self, mouse_pos: glm.vec2):
        if self.last_clicked_element:
            return self.last_clicked_element.handle_left_hold(mouse_pos)
        return False

    def handle_left_release(self, mouse_pos: glm.vec2):
        res = self.last_clicked_element is not None
        if self.last_clicked_element is not None:
            self.last_clicked_element.handle_left_release(mouse_pos)
        self.last_clicked_element = None
        return res

    def handle_right_click(self, mouse_pos: glm.vec2):
        element = self.find_clicked_element(mouse_pos)
        if self.active_sub_menu:
            self.active_sub_menu.active = False
            self.active_sub_menu = None

        if element.name == "Canvas":
            self.last_clicked_element = None
            return False
        else:
            element.handle_right_click(mouse_pos)
            self.last_clicked_element = element
            return True

    def handle_right_hold(self, mouse_pos: glm.vec2):
        if self.last_clicked_element:
            return self.last_clicked_element.handle_right_hold(mouse_pos)
        return False

    def handle_right_release(self, mouse_pos: glm.vec2):
        res = self.last_clicked_element is not None
        if self.last_clicked_element is not None:
            self.last_clicked_element.handle_right_release(mouse_pos)
        self.last_clicked_element = None
        return res

    def handle_keyboard_press(self, keys, pressed_char):
        if self.active_input_field:
            self.active_input_field.handle_keyboard_press(keys, pressed_char)
            return True
        return False

    def delete(self):
        self.canvas.delete()
        self.canvas = None
