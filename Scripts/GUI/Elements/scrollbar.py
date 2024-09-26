import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.Elements.block as block_m
import Scripts.GUI.Elements.text as text_m
import glm


# Не реализованно

class Scrollbar(element_m.Element):
    def __init__(self, name, rely_element, relative_left_bottom, win_size, relative_right_top=glm.vec2(1, 1),
                 size: glm.vec2 = None,
                 color=(0.7, 0.7, 0.7, 0.5),
                 background_color=(0.1, 0.1, 0.1, 0.1),
                 start_from_top=True,
                 space_between=0,
                 text_size=0.02
                 ):
        super().__init__(name, rely_element, relative_left_bottom, win_size, relative_right_top, size)

        # GUI
        self.space_between = space_between
        width = 0.05
        height = 0.15
        rlb = relative_left_bottom + glm.vec2(0, 0)
        rrt = rlb + glm.vec2(width, height)
        self.rlb_element_container = 0.0

        if start_from_top:
            rlb.y += 0.5
            rrt.y = relative_right_top.y
        self.scrollbar = block_m.Block("scrollbar", self, relative_left_bottom=rlb,
                                       relative_right_top=rrt,
                                       color=color,
                                       win_size=win_size

                                       )

        rlb = glm.vec2(rrt.x, relative_left_bottom.y)
        rrt = relative_right_top
        self.container = block_m.Block("container", self,
                                       relative_left_bottom=rlb,
                                       relative_right_top=rrt,
                                       color=background_color,
                                       win_size=win_size
                                       )

        # Other
        self.container_data = self.container.elements

    def render(self):
        self.get_m_gui()
        super().render()

    def add_element(self, text):
        pass
        # element_name = f"element_{len(self.container_data)}"
        # element_text = text_m.Text(f'{element_name}_text', text,
        #                            relative_left_bottom=,
        #                            )
        #
        # element = block_m.Block(element_name,
        #                         self.container,
        #                         self.rlb_element_container
        #                         )
        #
        # self.container_data.append(element)
