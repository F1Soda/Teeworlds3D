import Scripts.Source.General.GSM.game_state as state_m
import asyncio


class Connection(state_m.GameState):
    NAME = "Connection"

    def __init__(self, app, gsm):
        super().__init__(gsm, app)
        self.gui = app.gui
        self.socket = None

    def enter(self, params=None):
        if params is None:
            server_ip = "localhost"
            port = 9000
        else:
            server_ip, port = params
        connected = asyncio.run(self.fsm.client.connect())
        if not connected:
            self.fsm.set_state("Menu", f"Fail connect to {server_ip}:{port}")

    def render_level(self):
        self.app.ctx.screen.use()
        self.app.ctx.clear(color=(0.357, 0.502, 0.11, 1))

    def before_exit(self):
        self.app.exit()
