import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.Elements.elements as elements
import glm


class Inspector(element_m.Element):
    def __init__(self, gui, main_block):
        super().__init__('Inspector', main_block, gui.win_size)
        self.gui = gui
        self.main_block = main_block

        self.position.relative.left_bottom = glm.vec2(gui.LEFT_INSPECTOR_CORNER,
                                                      gui.DIVISION_BETWEEN_INSPECTOR_AND_HIERARCHY)
        self.position.relative.right_top = glm.vec2(1)

        background = elements.Block("Background", self, self.win_size, (0.1, 0.3, 0.1, 0.5))
        background.position.relative.right_top = glm.vec2(1)
        self.update_position()

        text_header = elements.Text("Header Text", background, self.win_size,
                                    "Inspector",
                                    centered_x=True,
                                    centered_y=True,
                                    font_size=2,
                                    space_between=0.1,
                                    pivot=element_m.Pivot.Center
                                    )
        text_header.position.relative.center = glm.vec2(0.5, 0.95)
        self.update_position()

    def delete(self):
        self.gui = None
        self.main_block = None
        super().delete()
