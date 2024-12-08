import Scripts.Source.General.GSM.game_state as state_m
import asyncio


class Connection(state_m.GameState):
    NAME = "Connection"

    def __init__(self, app, gsm):
        super().__init__(gsm, app)
        self.gui = app.gui

    def enter(self, params=None):
        if not self.fsm.client.connected:
            self.fsm.set_state("Menu", f"Attempt to load level without connection")
        if params is None:
            self.fsm.set_state("Menu", f"Internal Error: no level filepath")

        self.fsm.set_state("Game", (params, (0, 1, 0)))


    def render_level(self):
        self.app.ctx.screen.use()
        self.app.ctx.clear(color=(0.357, 0.502, 0.11, 1))

    def before_exit(self):
        self.app.exit()
