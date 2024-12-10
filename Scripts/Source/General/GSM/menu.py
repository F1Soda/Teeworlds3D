import Scripts.Source.General.GSM.game_state as state_m
import Scripts.Source.GUI.Menu.MenuSM.menu_sm as menu_sm_m
import moderngl as mgl


class Menu(state_m.GameState):
    NAME = "Menu"

    def __init__(self, app, gsm):
        super().__init__(gsm, app)
        self.gui = app.gui
        self.menu_sm = None

    def enter(self, params=None):
        self.menu_sm = menu_sm_m.MenuSM(self.app, self.fsm)
        if params:
            print("Menu | passed params: ", params)

    def exit(self):
        self.menu_sm.release()
        self.menu_sm = None

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
