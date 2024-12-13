import Scripts.Source.GUI.Game.GameSM.game_state as game_state_m
import Scripts.Source.GUI.Elements.element as element_m
import Scripts.Source.GUI.Elements.elements as elements
import glm

Pivot = element_m.Pivot


class GameDied(game_state_m.GameState):
    NAME = "DIED"

    def __init__(self, menu_sm, gsm):
        super().__init__(menu_sm)
        win_size = menu_sm.app.win_size
        self.gsm = gsm
        canvas = menu_sm.gui.canvas

        self.win_size = glm.vec2(win_size)
        self.aspect_ratio = win_size[0] / win_size[1]

        background = elements.Block("background", canvas, win_size, glm.vec4(0.2))
        background.position.relative.right_top = glm.vec2(1)
        background.update_position()
        self.elements.append(background)

        die_label = elements.Text("die label", background, win_size,
                                  "You DIED!", font_size=3)
        die_label.pivot = element_m.Pivot.Center
        die_label.position.relative.center = glm.vec2(0.5, 0.6)

        die_label.update_position()

        self.die_info = elements.Text("die label", background, win_size,
                                      "", font_size=1.5)
        self.die_info.pivot = element_m.Pivot.Center
        self.die_info.position.relative.center = glm.vec2(0.5, 0.45)

        self.die_info.update_position()

        def respawn_button_action(button, gui, pos):
            self.gsm.state.send_request_to_spawn()

        respawn_button = elements.Button("Respawn button", background, win_size, self,
                                         "Respawn",
                                         action=respawn_button_action,
                                         color=glm.vec4(0.7, 0.7, 0, 1),
                                         text_color=glm.vec4(1, 1, 1, 1),
                                         text_size=2
                                         )

        respawn_button.pivot = Pivot.Center
        respawn_button.position.relative.size = glm.vec2(0.15, 0.05)
        respawn_button.position.relative.center = glm.vec2(0.5, 0.45)

        respawn_button.update_position()

        self.exit()

        canvas.update_position()

    def set_die_info(self, message):
        self.die_info.text = message
        self.die_info.position.relative.center = glm.vec2(0.5, 0.3)
        self.die_info.update_position()
        return True

    def release(self):
        self.gsm = None
        for element in self.elements:
            element.delete()
