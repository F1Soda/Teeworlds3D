import Scripts.Source.GUI.Menu.MenuSM.menu_state as menu_state_m
import Scripts.Source.GUI.Elements.elements as elements
import Scripts.Source.GUI.Elements.element as element_m
import glm
import copy
import os


class MenuEditor(menu_state_m.MenuState):
    NAME = "EDITOR"

    def __init__(self, menu_sm, gsm):
        super().__init__(menu_sm)
        win_size = menu_sm.app.win_size
        self.gsm = gsm
        canvas = menu_sm.gui.canvas

        self.selected_level_button = None
        self.selected_level_path = None

        def back_button_action(button, gui, pos):
            self.fsm.set_state("WELCOME")

        back_button = elements.Button("Back Button", canvas, win_size, self,
                                      "<<",
                                      action=back_button_action,
                                      color=glm.vec4(0.7, 0.1, 0.1, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=2
                                      )

        back_button.position.relative.center = glm.vec2(0.03, 0.9)
        back_button.position.relative.size = glm.vec2(0.04, 0.07)
        back_button.position.evaluate_values_by_relative()
        self.elements.append(back_button)

        levels_label = elements.Text("levels label", canvas, win_size,
                                     "Levels", font_size=3)
        levels_label.pivot = element_m.Pivot.LeftBottom
        levels_label.position.relative.center = glm.vec2(0.15, 0.9)
        self.elements.append(levels_label)

        rcp = glm.vec2(0.03, 0.74)

        def load_button_action(button, gui, pos):
            if self.selected_level_button is not None:
                self.exit()
                self.gsm.set_state("Editor", self.selected_level_button.value)

        load_button = elements.Button("Load Button", canvas, win_size, self,
                                      "Load",
                                      action=load_button_action,
                                      color=glm.vec4(0.7, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=2
                                      )
        load_button.position.relative.center = copy.copy(rcp)
        load_button.position.relative.size = glm.vec2(0.15, 0.05)
        self.elements.append(load_button)

        rcp.y -= 0.07

        def create_button_action(button, gui, pos):
            self.exit()
            self.gsm.set_state("Editor", None)

        create_button = elements.Button("Create Button", canvas, win_size, self,
                                        "Create",
                                        action=create_button_action,
                                        color=glm.vec4(0.7, 0.7, 0, 1),
                                        text_color=glm.vec4(1, 1, 1, 1),
                                        text_size=2
                                        )
        create_button.position.relative.center = copy.copy(rcp)
        create_button.position.relative.size = glm.vec2(0.15, 0.05)
        self.elements.append(create_button)

        rcp.y -= 0.07

        def copy_button_action(button, gui, pos):
            pass

        copy_button = elements.Button("Copy Button", canvas, win_size, self,
                                      "Copy",
                                      action=copy_button_action,
                                      color=glm.vec4(0.7, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=2
                                      )
        copy_button.position.relative.center = copy.copy(rcp)
        copy_button.position.relative.size = glm.vec2(0.15, 0.05)
        self.elements.append(copy_button)

        rcp.y -= 0.07

        def delete_button_action(button, gui, pos):
            pass

        delete_button = elements.Button("Delete Button", canvas, win_size, self,
                                        "Delete",
                                        action=delete_button_action,
                                        color=glm.vec4(0.7, 0.7, 0, 1),
                                        text_color=glm.vec4(1, 1, 1, 1),
                                        text_size=2
                                        )
        delete_button.position.relative.center = copy.copy(rcp)
        delete_button.position.relative.size = glm.vec2(0.15, 0.05)
        self.elements.append(delete_button)

        self.servers_block = elements.Block("Levels Block", canvas, win_size, glm.vec4(0.3, 0.3, 0.3, 0.3))
        self.servers_block.position.relative.left_bottom = glm.vec2(rcp.x + copy_button.position.relative.size.x + 0.01,
                                                                    0.15)
        self.servers_block.position.relative.right_top = glm.vec2(0.7, load_button.position.relative.right_top.y)
        self.elements.append(self.servers_block)

        canvas.update_position()

        self.level_content = elements.Content("Server Content", self.servers_block, win_size)
        self.level_content.position.relative.center = glm.vec2(0.5, 1)
        # self.level_content.position.relative.right_top = glm.vec2(1)
        self.level_content.pivot = element_m.Pivot.Top
        self.level_content.position.evaluate_values_by_relative()
        self.update_level_list()
        self.elements.append(self.level_content)

        self.exit()

        canvas.update_position()

    def update_level_list(self):
        # self.level_content.clear()
        levels = []
        for filename in os.listdir("Levels/Base"):
            if filename.endswith('.json'):
                file_path = os.path.join("Levels/Base", filename)
                levels.append((filename[:-5], file_path))
        for filename in os.listdir("Levels/Player"):
            if filename.endswith('.json'):
                file_path = os.path.join("Levels/Player", filename)
                levels.append((filename[:-5], file_path))

        def select_action(button, gui, pos):
            name = button.rely_element.name

            button.color = glm.vec4(0.6, 0.6, 0.6, 1)

            if self.selected_level_button is not None and self.selected_level_button is not button:
                self.selected_level_button.color = glm.vec4(0.7, 0.7, 0.7, 1)
            self.selected_level_button = button
            # self.selected_elements.append((button, obj_id))

        for level in levels:
            self._create_element_in_content(self.level_content,
                                            glm.vec2(self.servers_block.position.relative_window.size.x, 0.03),
                                            select_action, level[0], level[1])

    def _create_element_in_content(self, content, size, action, text, value):
        content_element = elements.Block(f"Element_in_content_{content.name}", None, self.fsm.app.win_size,
                                         (1, 1, 1, 0.5))
        content_element.position.relative_window.size = size
        content_element.position.evaluate_values_by_relative_window()

        button = elements.Button(f"{text}_Button", content_element, self.fsm.app.win_size, self,
                                 text,
                                 action=action,
                                 color=glm.vec4(0.7, 0.7, 0.7, 1),
                                 text_size=1,
                                 value=value
                                 )

        button.position.relative.left_bottom = glm.vec2(0)
        button.position.relative.right_top = glm.vec2(1)
        button.position.evaluate_values_by_relative()
        button.update_position()

        content.add(content_element)
        content.update_position()
