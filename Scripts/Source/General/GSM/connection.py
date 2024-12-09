import Scripts.Source.General.GSM.game_state as state_m
import asyncio


class Connection(state_m.GameState):
    NAME = "Connection"

    def __init__(self, app, gsm):
        super().__init__(gsm, app)
        self.gui = app.gui

    def enter(self, params=None):
        # if not self.fsm.network.connected:
        #     self.fsm.set_state("Menu", f"Attempt to load level without connection")
        # if params is None:
        #     self.fsm.set_state("Menu", f"Internal Error: no level filepath")

        request_to_spawn = {"action": "spawn"}

        response = self.fsm.app.network.send(request_to_spawn)
        print(response)
        self.fsm.set_state("Game", ("Levels/Player/TestCollision.json", response["spawn_pos"], response["state"]))

    def render_level(self):
        self.app.ctx.screen.use()
        self.app.ctx.clear(color=(0.357, 0.502, 0.11, 1))

    def before_exit(self):
        self.app.exit()
