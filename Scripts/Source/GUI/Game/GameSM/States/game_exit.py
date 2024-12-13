import Scripts.Source.GUI.Game.GameSM.game_state as game_state_m
import Scripts.Source.GUI.Elements.element as element_m
import Scripts.Source.GUI.Elements.elements as elements
import glm

Pivot = element_m.Pivot


class GameExit(game_state_m.GameState):
    NAME = "EXIT"

    def __init__(self, menu_sm, gsm):
        super().__init__(menu_sm)
        win_size = menu_sm.app.win_size
        self.gsm = gsm
        canvas = menu_sm.gui.canvas

        self.win_size = glm.vec2(win_size)
        self.aspect_ratio = win_size[0] / win_size[1]

        background = elements.Block("background", canvas, win_size, glm.vec4(0.4))
        background.position.relative.size = glm.vec2(0.2, 0.3)
        background.position.relative.center = glm.vec2(0.5)
        background.update_position()
        self.elements.append(background)

        menu_label = elements.Text("menu label", background, win_size,
                                   "Pause", font_size=3)
        menu_label.pivot = element_m.Pivot.Center
        menu_label.position.relative.center = glm.vec2(0.5, 0.8)

        button_size = glm.vec2(0.8, 0.15)
        gaps = 0.05

        rcp = glm.vec2(0.5, 0.6)

        menu_label.update_position()

        def continue_button_action(button, gui, pos):
            ...

        continue_button = elements.Button("Continue Button", background, win_size, self,
                                          "Continue",
                                          action=continue_button_action,
                                          color=glm.vec4(0.7, 0.7, 0, 1),
                                          text_color=glm.vec4(1, 1, 1, 1),
                                          text_size=1.5
                                          )
        continue_button.position.relative.size = button_size
        continue_button.position.relative.center = rcp.xy

        continue_button.update_position()

        rcp.y -= button_size.y + gaps

        def back_to_menu_button_action(button, gui, pos):
            pass

        menu_button = elements.Button("Menu Button", background, win_size, self,
                                      "Menu",
                                      action=back_to_menu_button_action,
                                      color=glm.vec4(0.7, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=1.5
                                      )

        menu_button.position.relative.size = button_size

        menu_button.position.relative.center = rcp.xy

        menu_button.update_position()

        rcp.y -= button_size.y + gaps

        def exit_button_action(button, gui, pos):
            ...

        exit_button = elements.Button("Exit Button", background, win_size, self,
                                      "Exit",
                                      action=exit_button_action,
                                      color=glm.vec4(0.7, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=1.5
                                      )

        exit_button.position.relative.size = button_size
        exit_button.position.relative.center = rcp.xy

        exit_button.update_position()

        self.exit()

        canvas.update_position()

    def release(self):
        self.gsm = None
        for element in self.elements:
            element.delete()
