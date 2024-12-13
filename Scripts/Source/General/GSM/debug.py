import Scripts.Source.General.GSM.game_state as state_m
import moderngl as mgl


class Debug(state_m.GameState):
    NAME = "Debug"

    def __init__(self, app, gsm):
        super().__init__(gsm, app)
        self.gui = app.gui
        self.menu_sm = None
        self.socket = None

    def enter(self, params=None):
        if params is None:
            level = "Levels/Player/TestCollision.json"
        else:
            level = params

        self.fsm.set_state("Game", (level, (0, 3, 0), {}, "default"))
