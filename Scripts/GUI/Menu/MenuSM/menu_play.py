import Scripts.GUI.Menu.MenuSM.menu_state as menu_state_m
import Scripts.GUI.Elements.elements as elements
import Scripts.GUI.Elements.element as element_m
import glm
import copy


class MenuPlay(menu_state_m.MenuState):
    NAME = "PLAY"

    def __init__(self, menu_sm, gsm):
        super().__init__(menu_sm)
        win_size = menu_sm.app.win_size
        self.gsm = gsm
        canvas = menu_sm.gui.canvas

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
            pass

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

        servers_block = elements.Block("Servers Block", canvas, win_size, glm.vec4(0.3, 0.3, 0.3, 0.3))
        servers_block.position.relative.left_bottom = glm.vec2(rcp.x + host_button.position.relative.size.x + 0.01, rcp.y)
        servers_block.position.relative.right_top = glm.vec2(0.7, connect_button.position.relative.right_top.y)
        self.elements.append(servers_block)

        self.exit()

        canvas.update_position()
