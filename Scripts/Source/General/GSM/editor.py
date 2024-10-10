import Scripts.Source.General.GSM.game_state as state_m
import Scripts.Source.General.Game.level as level_m
import Scripts.GUI.Editor.editor_gui as editorGUI_m
import Scripts.Source.Render.gizmos as gizmos_m
import Scripts.Source.General.Managers.object_picker as object_picker_m
import Scripts.Source.General.Managers.object_creator as object_creator_m

import moderngl as mgl

# possible not working
import pygame as pg


class Editor(state_m.GameState):
    NAME = "Editor"

    def __init__(self, app, gsm):
        super().__init__(gsm, app)
        self.level = None
        self.gizmos = None
        self.editor_gui = None
        self.gui = app.gui
        self.ctx = self.app.ctx
        self.win_size = self.app.win_size

        self.draw_gui = True

    @property
    def time(self):
        return self.app.time

    @property
    def delta_time(self):
        return self.app.delta_time

    def load_level(self, file_path=None):
        if self.level:
            self.level.delete()
            object_picker_m.ObjectPicker.release()
            object_creator_m.ObjectCreator.release()
        if self.gizmos:
            self.gizmos.delete()
        self.level = level_m.Level(self, self.gui)

        object_creator_m.ObjectCreator.rely_level = self.level
        object_picker_m.ObjectPicker.init(self)
        self.level.load(file_path)
        self.gizmos = gizmos_m.Gizmos(self.ctx, self.level)

        self.editor_gui.update_data_in_hierarchy()

    def process_window_resize(self, new_size):
        self.win_size = new_size
        self.editor_gui.process_window_resize(new_size)
        self.level.process_window_resize(new_size)
        self.gizmos.process_window_resize(new_size)
        object_picker_m.ObjectPicker.process_window_resize(new_size)

    def update(self):
        self.level.apply_components()
        object_picker_m.ObjectPicker.picking_pass()

    def fixed_update(self):
        self.level.fixed_apply_components()

    def render_level(self):
        self.app.ctx.screen.use()
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        self.ctx.enable(mgl.BLEND)
        self.level.render_opaque_objects()

        self.level.render_transparent_objects()

    def render_gizmo(self):
        self.app.ctx.screen.use()
        self.gizmos.render()

    def render_gui(self):
        if self.draw_gui:
            self.app.ctx.screen.use()
            self.ctx.disable(mgl.DEPTH_TEST)
            self.ctx.enable(mgl.BLEND)
            self.gui.render()
            self.ctx.disable(mgl.BLEND)
            self.ctx.enable(mgl.DEPTH_TEST)

    def before_exit(self):
        self.editor_gui.ask_save_file_before_exit()

    def close_app(self):
        self.app.exit()

    def exit(self):
        self.level.delete()
        self.gizmos.delete()
        self.editor_gui.delete()

        object_picker_m.ObjectPicker.release()
        object_creator_m.ObjectCreator.release()

    def enter(self, params=None):
        # GUI
        self.editor_gui = editorGUI_m.EditorGUI(self, self.app.win_size, self.app.gui)
        self.load_level(params)
