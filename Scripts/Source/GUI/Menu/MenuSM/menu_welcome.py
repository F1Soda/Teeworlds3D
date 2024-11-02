import Scripts.Source.GUI.Menu.MenuSM.menu_state as menu_state_m
import Scripts.Source.GUI.Elements.elements as elements
import Scripts.Source.GUI.Elements.element as element_m
import glm
import copy


class MenuWelcome(menu_state_m.MenuState):
    NAME = "WELCOME"

    def __init__(self, menu_sm):
        super().__init__(menu_sm)
        win_size = menu_sm.app.win_size

        canvas = menu_sm.gui.canvas


        rcp = glm.vec2(0.01, 0.7)

        teeworlds_label = elements.Text("teeworlds_label", canvas, win_size,
                                        "TEEWORLDS 3D", font_size=3)
        teeworlds_label.pivot = element_m.Pivot.LeftBottom
        teeworlds_label.position.relative.center = glm.vec2(0.01, 0.6)
        self.elements.append(teeworlds_label)

        rcp = glm.vec2(0.03, 0.54)

        def play_button_action(button, gui, pos):
            self.fsm.set_state("PLAY")

        play_button = elements.Button("Play Button", canvas, win_size, self,
                                      "Play",
                                      action=play_button_action,
                                      color=glm.vec4(0.7, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=2
                                      )
        play_button.position.relative.center = copy.copy(rcp)
        play_button.position.relative.size = glm.vec2(0.2, 0.05)
        play_button.position.evaluate_values_by_relative()
        self.elements.append(play_button)

        rcp.y -= 0.06

        def editor_button_action(button, gui, pos):
            self.fsm.set_state("EDITOR")

        editor_button = elements.Button("Editor Button", canvas, win_size, self,
                                        "Editor",
                                        action=editor_button_action,
                                        color=glm.vec4(0.7, 0.7, 0, 1),
                                        text_color=glm.vec4(1, 1, 1, 1),
                                        text_size=2
                                        )
        editor_button.position.relative.center = copy.copy(rcp)
        editor_button.position.relative.size = glm.vec2(0.2, 0.05)
        editor_button.position.evaluate_values_by_relative()
        self.elements.append(editor_button)
        rcp.y -= 0.06

        def settings_button_action(button, gui, pos):
            pass

        settings_button = elements.Button("Settings Button", canvas, win_size, self,
                                          "Settings",
                                          action=settings_button_action,
                                          color=glm.vec4(0.7, 0.7, 0, 1),
                                          text_color=glm.vec4(1, 1, 1, 1),
                                          text_size=2
                                          )
        settings_button.position.relative.center = copy.copy(rcp)
        settings_button.position.relative.size = glm.vec2(0.2, 0.05)
        settings_button.position.evaluate_values_by_relative()
        self.elements.append(settings_button)

        self.exit()

        canvas.update_position()

