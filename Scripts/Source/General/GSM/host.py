import Scripts.Source.General.GSM.game_state as state_m
import moderngl as mgl


class Host(state_m.GameState):
    NAME = "Host"

    def __init__(self, app, gsm):
        super().__init__(gsm, app)
        self.gui = app.gui
        self.menu_sm = None
        self.socket = None

    def enter(self, params=None):
        ip, port, level_path = params

    def try_to_host(self, ip, port, level_path):
        ...

    def exit(self):
        self.menu_sm.release()

    def render_level(self):
        self.app.ctx.screen.use()
        self.app.ctx.clear(color=(0.357, 0.502, 0.11, 1))

    def render_gui(self):
        self.app.ctx.screen.use()
        self.app.ctx.disable(mgl.DEPTH_TEST)
        self.app.ctx.enable(mgl.BLEND)
        self.gui.render()

    def before_exit(self):
        self.app.exit()