import Scripts.Source.General.Managers.object_creator as object_creator_m
import Scripts.Source.General.GSM.game_state as state_m
import Scripts.GUI.Game.game_gui as game_gui_m
import Scripts.Source.General.Game.level as level_m
import moderngl as mgl
import pygame as pg


class Game(state_m.GameState):
    NAME = "Game"

    def __init__(self, app, gsm):
        super().__init__(gsm, app)
        self.level = None
        self.game_gui = None
        self.gui = app.gui
        self.ctx = self.app.ctx
        self.win_size = self.app.win_size

    @property
    def time(self):
        return self.app.time

    @property
    def delta_time(self):
        return self.app.delta_time

    def _load_level(self, file_path=None):
        if self.level:
            self.level.delete()

        self.level = level_m.Level(self, self.gui)
        object_creator_m.ObjectCreator.rely_level = self.level
        self.level.load(file_path,  is_game=True)

    def enter(self, params=None):
        self.game_gui = game_gui_m.GameGUI(self, self.app.win_size, self.app.gui)
        if params is None:
            params = "Levels/Base/Empty.json"
        self._load_level(params)
        self.app.grab_mouse_inside_bounded_window = True
        self.app.set_mouse_visible(False)
        self.app.set_mouse_grab(True)

    def exit(self):
        self.level.delete()
        self.game_gui.delete()

    def _render(self):
        self.ctx.screen.use()
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        self.ctx.enable(mgl.BLEND)
        self.level.render_opaque_objects()

        self.level.render_transparent_objects()
        self.ctx.enable(mgl.BLEND)
        self.ctx.disable(mgl.DEPTH_TEST)

        # GUI
        self.gui.render()
        self.ctx.disable(mgl.BLEND)
        self.ctx.enable(mgl.DEPTH_TEST)
        pg.display.flip()

    def before_exit(self):
        self.app.exit()

    def update(self):
        self.app.ctx.screen.use()
        self.level.apply_components()
        self._render()

    def process_window_resize(self, new_size):
        self.win_size = new_size
