import Scripts.GUI.Elements.element as element_m
import glm


# Settings
DEV_MODE = True

Pivot = element_m.Pivot


class GameGUI:

    def __init__(self, game, win_size, gui):
        self.game = game
        self.win_size = glm.vec2(win_size)
        self.aspect_ratio = win_size[0] / win_size[1]
        self.gui = gui

    @property
    def windows(self):
        return self.gui.windows

    def process_window_resize(self, new_size):
        self.win_size = new_size

    def delete(self):
        self.game = None
        self.gui = None
