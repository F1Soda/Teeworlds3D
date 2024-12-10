import Scripts.Source.General.GSM.game_state as state_m
import asyncio


class Connection(state_m.GameState):
    NAME = "Connection"

    def __init__(self, app, gsm):
        super().__init__(gsm, app)
        self.gui = app.gui

    def enter(self, params=None):
        request_to_spawn = {"actions": {"spawn": None}}

        response = self.fsm.app.network.send(request_to_spawn)

        if response is None:
            self.fsm.set_state("Menu", f"Fail connect to server")
        else:
            spawn_pos = response["actions"]["spawn"]["spawn_pos"]
            self.fsm.set_state("Game", ("Levels/Player/TestCollision.json", spawn_pos, response["game_state"]))

    def render_level(self):
        self.app.ctx.screen.use()
        self.app.ctx.clear(color=(0.357, 0.502, 0.11, 1))

    def before_exit(self):
        self.app.exit()
