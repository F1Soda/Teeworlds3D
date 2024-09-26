import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.Elements.block as block_m
import copy
import glm


class Content(element_m.Element):
    def __init__(self, name, rely_element, win_size: glm.vec2, color=(0, 0, 0, 0.1)):
        super().__init__(name, rely_element, win_size)

        self.background = block_m.Block(f"{name}_block", self, win_size, color)
        self.background.position.relative.right_top = glm.vec2(1)
        self.background.position.evaluate_values_by_relative()
        self.elements_size = []
        self.add_to_bottom = False
        self.active = False

    def add(self, element):
        new_size_y = self.position.absolute.size.y + element.position.absolute.size.y

        # Self and Background settings
        past_center = copy.copy(self.position.absolute.center)
        self.position.absolute.size = glm.vec2(max(self.position.absolute.size.x, element.position.absolute.size.x),
                                               new_size_y)
        self.position.absolute.center = past_center

        if self.pivot == element_m.Pivot.Top:
            self.position.absolute.transform(glm.vec2(0, -element.position.absolute.size.y / 2))

        self.position.evaluate_values_by_absolute()
        self.background.position.evaluate_values_by_relative()

        current_left_bottom = 0

        for i in range(len(self.background.elements)):
            size_y = self.elements_size[i].y / new_size_y

            self.background.elements[i].position.relative.left_bottom = glm.vec2(0, current_left_bottom)
            self.background.elements[i].position.relative.size = glm.vec2(
                self.background.elements[i].position.relative.size.x, size_y)
            current_left_bottom += size_y
            self.background.elements[i].position.evaluate_values_by_relative()

        # Element settings
        element.rely_element = self.background
        element.position.rely_element_position = self.background.position
        if len(self.background.elements) == 0:
            element.position.absolute.left_bottom = copy.copy(self.background.position.absolute.left_bottom)
        else:
            element.position.absolute.left_bottom = glm.vec2(self.background.position.absolute.left_bottom.x,
                                                             self.background.elements[-1].position.absolute.right_top.y)

        element.position.absolute.right_top = copy.copy(self.background.position.absolute.right_top)
        element.position.evaluate_values_by_absolute()
        for inner_elements in element.elements:
            inner_elements.update_position()

        self.background.elements.append(element)

        self.elements_size.append(element.position.absolute.size)

    def render(self):
        if self.active:
            self.background.render()

    def clear(self):
        for element in self.background.elements:
            element.delete()
        self.background.elements.clear()
        self.elements_size.clear()
        if self.pivot == element_m.Pivot.Top:
            self.position.absolute.left_bottom = glm.vec2(self.position.absolute.left_bottom.x,
                                                          self.position.absolute.right_top.y)
        self.position.evaluate_values_by_absolute()
        self.update_position()

    def contains(self, name):
        for element in self.background.elements:
            if element.name == name:
                return True
        return False

    def delete(self):
        self.background = None
        self.elements_size.clear()
        super().delete()
