import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import glm
import pygame as pg
import moderngl as mgl

import Scripts.GUI.library as library_gui_m
import Scripts.Source.Render.library as library_object_m
import Scripts.Source.General.Managers.data_manager as data_manager_m
import Scripts.Source.General.Managers.input_manager as input_manager_m
import Scripts.Source.General.GSM.gsm as gsm_m

import Scripts.GUI.gui as canvas_m

WIN_SIZE = (1600, 900)


class TeeworldsEngine:
    win_size = glm.vec2()

    def __init__(self, width=WIN_SIZE[0], height=WIN_SIZE[1]):
        pg.init()

        # Window size
        TeeworldsEngine.win_size = glm.vec2(width, height)

        # Settings GL
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.win_size, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)

        # Context
        self.ctx = mgl.create_context()
        self.ctx.enable(mgl.DEPTH_TEST | mgl.CULL_FACE)

        # Transparency
        self.ctx.blend_func = mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA

        # Data Manager
        data_manager_m.DataManager.init()

        # Library
        library_gui_m.init(self.ctx)
        library_object_m.init(self.ctx)

        # Clock and time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        # Input Manager
        input_manager_m.InputManager.init(self)

        # GUI
        self.gui = canvas_m.GUI(self, self.win_size)

        pg.display.set_caption(f"Teeworlds3D")

        # Subscribe To Events
        input_manager_m.InputManager.handle_right_click_event += self.gui.handle_right_click
        input_manager_m.InputManager.handle_right_hold_event += self.gui.handle_right_hold
        input_manager_m.InputManager.handle_right_release_event += self.gui.handle_right_release

        input_manager_m.InputManager.handle_left_click_event += self.gui.handle_left_click
        input_manager_m.InputManager.handle_left_hold_event += self.gui.handle_left_hold
        input_manager_m.InputManager.handle_left_release_event += self.gui.handle_left_release

        input_manager_m.InputManager.handle_keyboard_press += self.gui.handle_keyboard_press

        # Game State Machine
        self.gsm = gsm_m.GSM(self)

    def process_window_resize(self, event):
        self.win_size = glm.vec2(event.size)
        pg.display.set_mode((self.win_size.x, self.win_size.y), flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        self.gui.process_window_resize(self.win_size)
        self.gsm.state.process_window_resize(self.win_size)
        self.ctx.viewport = (0, 0, self.win_size.x, self.win_size.y)

    def update_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def before_exit(self):
        self.gsm.state.before_exit()

    def exit(self):
        pg.quit()
        input_manager_m.InputManager.release()
        self.gsm.state.exit()
        sys.exit()

    def run(self):
        while True:
            self.delta_time = self.clock.tick(120)
            self.update_time()
            self.gsm.state.update()
            input_manager_m.InputManager.process()


if __name__ == '__main__':
    app = TeeworldsEngine()
    app.run()
