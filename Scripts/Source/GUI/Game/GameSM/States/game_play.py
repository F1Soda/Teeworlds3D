import Scripts.Source.GUI.Game.GameSM.game_state as game_state_m
import Scripts.Source.GUI.Elements.element as element_m
import Scripts.Source.GUI.library as library_m
import Scripts.Source.GUI.Elements.elements as elements
import glm

Pivot = element_m.Pivot


class GamePlay(game_state_m.GameState):
    NAME = "PLAY"

    def __init__(self, menu_sm, gsm):
        super().__init__(menu_sm)
        win_size = menu_sm.app.win_size
        self.gsm = gsm
        canvas = menu_sm.gui.canvas

        self.win_size = glm.vec2(win_size)
        self.aspect_ratio = win_size[0] / win_size[1]

        self.fps_text = elements.Text("FPS", canvas, self.win_size,
                                      "FPS: ",
                                      font_size=1,
                                      space_between=0.1,
                                      pivot=element_m.Pivot.LeftBottom
                                      )
        self.fps_text.position.relative.left_bottom = glm.vec2(0)
        self.fps_text.update_position()

        self.elements.append(self.fps_text)

        self.crosshair_texture = elements.Texture("Crosshair", canvas, self.win_size,
                                                  library_m.textures["crosshair"], False)
        self.crosshair_texture.pivot = Pivot.Center
        self.crosshair_size = 0.025
        self.crosshair_texture.position.relative.left_bottom = glm.vec2(0.5 - self.crosshair_size / 2,
                                                                        0.5 - self.aspect_ratio * self.crosshair_size / 2)

        self.crosshair_texture.position.relative.size = glm.vec2(self.crosshair_size,
                                                                 self.aspect_ratio * self.crosshair_size)

        self.crosshair_texture.update_position()

        self.elements.append(self.crosshair_texture)

        self.ammo_bar = elements.Text("Ammo bar", canvas, self.win_size,
                                      "Ammo: 30",
                                      font_size=2,
                                      space_between=0.1,
                                      pivot=element_m.Pivot.LeftBottom
                                      )
        self.ammo_bar.position.relative.left_bottom = glm.vec2(0.87, 0.03)
        self.ammo_bar.update_position()

        self.elements.append(self.ammo_bar)

    def set_ammo(self, ammo_count):
        self.ammo_bar.text = f"Ammo: {ammo_count}"

    def display_reloading(self):
        self.ammo_bar.text = f"Reloading"

    def release(self):
        self.gsm = None
        for element in self.elements:
            element.delete()
