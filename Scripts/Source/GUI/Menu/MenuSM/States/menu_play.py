import Scripts.Source.GUI.Menu.MenuSM.menu_state as menu_state_m
import Scripts.Source.GUI.Elements.elements as elements
import Scripts.Source.GUI.Elements.element as element_m
import glm
import copy

import Scripts.Source.GUI.library as library_m


class MenuPlay(menu_state_m.MenuState):
    NAME = "PLAY"

    def __init__(self, menu_sm, gsm):
        super().__init__(menu_sm)
        win_size = menu_sm.app.win_size
        self.gsm = gsm
        canvas = menu_sm.gui.canvas

        self.selected_level_button = None

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

        servers_label = elements.Text("servers_label", canvas, win_size,
                                      "Servers", font_size=3)
        servers_label.pivot = element_m.Pivot.LeftBottom
        servers_label.position.relative.center = glm.vec2(0.15, 0.9)
        self.elements.append(servers_label)

        rcp = glm.vec2(0.03, 0.74)

        def connect_button_action(button, gui, pos):
            if self.selected_level_button is not None:
                session = self.selected_level_button.value
                self.exit()
                self.gsm.set_state("Connection", session)

        connect_button = elements.Button("Connect Button", canvas, win_size, self,
                                         "Connect",
                                         action=connect_button_action,
                                         color=glm.vec4(0.7, 0.7, 0, 1),
                                         text_color=glm.vec4(1, 1, 1, 1),
                                         text_size=2
                                         )
        connect_button.position.relative.center = copy.copy(rcp)
        connect_button.position.relative.size = glm.vec2(0.15, 0.05)
        self.elements.append(connect_button)

        rcp.y -= 0.07

        def update_button_action(button, gui, pos):
            pass

        update_button = elements.Button("Update Button", canvas, win_size, self,
                                        "Update",
                                        action=update_button_action,
                                        color=glm.vec4(0.7, 0.7, 0, 1),
                                        text_color=glm.vec4(1, 1, 1, 1),
                                        text_size=2
                                        )
        update_button.position.relative.center = copy.copy(rcp)
        update_button.position.relative.size = glm.vec2(0.15, 0.05)
        self.elements.append(update_button)

        rcp.y = 0.1

        def host_button_action(button, gui, pos):
            self.exit()
            self.gsm.set_state("Game")

        host_button = elements.Button("Host Button", canvas, win_size, self,
                                      "Host",
                                      action=host_button_action,
                                      color=glm.vec4(0.7, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=2
                                      )

        host_button.position.relative.center = copy.copy(rcp)
        host_button.position.relative.size = glm.vec2(0.15, 0.05)
        self.elements.append(host_button)

        self.servers_block = elements.Block("Servers Block", canvas, win_size, glm.vec4(0.3, 0.3, 0.3, 0.3))
        self.servers_block.position.relative.left_bottom = glm.vec2(rcp.x + host_button.position.relative.size.x + 0.01,
                                                                    rcp.y)
        self.servers_block.position.relative.right_top = glm.vec2(0.7, connect_button.position.relative.right_top.y)

        self.elements.append(self.servers_block)

        canvas.update_position()

        self.server_info_block = elements.Block("Server info block", canvas, win_size, glm.vec4(0.3, 0.3, 0.3, 0.3))
        self.server_info_block.position.relative.right_top = glm.vec2(0.98,
                                                                      connect_button.position.relative.right_top.y)
        self.server_info_block.position.relative.left_bottom = glm.vec2(0.72,
                                                                        self.servers_block.position.relative.left_bottom.y)

        self.elements.append(self.server_info_block)

        canvas.update_position()

        self.server_info_text = elements.Text("server_info_text", self.server_info_block, win_size,
                                              "", font_size=1)
        self.server_info_text.pivot = element_m.Pivot.LeftBottom
        self.server_info_text.position.relative.center = glm.vec2(0.05, 0.66)

        self.screenshot_server_info = elements.Texture("default_map_screen", self.server_info_block, win_size,
                                                       library_m.textures["default_map_screen"], False)
        # self.screenshot_server_info.pivot = element_m.Pivot.Center
        self.screenshot_server_info.position.relative.left_bottom = glm.vec2(0.05, 0.7)
        self.screenshot_server_info.position.relative.right_top = glm.vec2(0.95, 0.99)

        # self.screenshot_server_info.position.relative.size = glm.vec2(1, 0.5) * 0.5

        self.screenshot_server_info.update_position()

        self.screenshot_server_info.active = False

        self.level_content = elements.Content("Server Content", self.servers_block, win_size)
        self.level_content.position.relative.center = glm.vec2(0.5, 1)
        # self.level_content.position.relative.right_top = glm.vec2(1)
        self.level_content.pivot = element_m.Pivot.Top
        self.level_content.position.evaluate_values_by_relative()

        self.elements.append(self.level_content)

        self.exit()

        canvas.update_position()

    def exit(self):
        super().exit()
        self.selected_level_button = None
        self.server_info_text.text = ""
        self.screenshot_server_info.active = False

    def enter(self, params=None):
        super().enter(params)

        if self.gsm.network.id == -1:
            self.gsm.network.connect()

        self.level_content.clear()

        def select_action(button, gui, pos):
            name = button.rely_element.name

            button.color = glm.vec4(0.6, 0.6, 0.6, 1)

            if self.selected_level_button is not None and self.selected_level_button is not button:
                self.selected_level_button.color = glm.vec4(0.7, 0.7, 0.7, 1)
            self.selected_level_button = button

            session = self.selected_level_button.value

            text = (f"Name: {session["name"]}\n"
                    f"Players: {session["count_players"]}/{session["max_count"]}\n"
                    f"Level: {session["level"]}\n"
                    f"Mode: {session["mode"]}")

            self.server_info_text.text = text
            self.screenshot_server_info.active = True

            # self.selected_elements.append((button, obj_id))

        for session in self.fsm.app.network.sessions:
            self._create_element_in_content(self.level_content,
                                            glm.vec2(self.servers_block.position.relative_window.size.x, 0.03),
                                            select_action, session["name"], session)

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
