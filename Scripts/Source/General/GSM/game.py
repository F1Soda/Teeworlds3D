import Scripts.Source.General.Managers.object_creator as object_creator_m
import Scripts.Source.General.GSM.game_state as state_m
import Scripts.GUI.Game.game_gui as game_gui_m
import Scripts.GUI.Editor.editor_gui as editor_gui_m
import Scripts.Source.General.Game.level as level_m
import Scripts.Source.Render.gizmos as gizmos_m
import moderngl as mgl
import pygame as pg


class Game(state_m.GameState):
    NAME = "Game"

    def __init__(self, app, gsm):
        super().__init__(gsm, app)
        self.level = None
        self.gizmos = None
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

    def get_fps(self):
        return self.app.get_fps()

    def _load_level(self, file_path=None):
        if self.level:
            self.level.delete()
        if self.gizmos:
            self.gizmos.delete()
        self.gizmos = []
        self.level = level_m.Level(self, self.gui)
        object_creator_m.ObjectCreator.rely_level = self.level
        self.level.load(file_path, is_game=True)

        # self.gizmos = gizmos_m.Gizmos(self.ctx, self.level)

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
        # self.gizmos.delete()
        self.game_gui.delete()

    def before_exit(self):
        self.app.exit()

    def update(self):
        self.level.apply_components()

    def fixed_update(self):
        self.level.fixed_apply_components()

    def render_level(self):
        self.app.ctx.screen.use()
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        self.ctx.enable(mgl.BLEND)
        self.level.render_opaque_objects()

        self.level.render_transparent_objects()

    def render_gizmo(self):
        for gizmo in self.gizmos:
            gizmo.apply()

    def render_gui(self):
        self.app.ctx.screen.use()
        self.ctx.disable(mgl.DEPTH_TEST)
        self.gui.render()
        self.ctx.disable(mgl.BLEND)
        self.ctx.enable(mgl.DEPTH_TEST)

    def process_window_resize(self, new_size):
        self.win_size = new_size
        self.game_gui.process_window_resize(new_size)
        self.gizmos.process_window_resize(new_size)
