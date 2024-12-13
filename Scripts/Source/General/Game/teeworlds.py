import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import Scripts.Source.GUI.library as library_gui_m
import Scripts.Source.Render.library as library_object_m
import Scripts.Source.General.Managers.data_manager as data_manager_m
import Scripts.Source.General.Managers.input_manager as input_manager_m
import Scripts.Source.General.GSM.gsm as gsm_m
import Scripts.Source.GUI.gui as canvas_m
import Scripts.Source.Multiplayer.network as network_m
import glm
import pygame as pg
import moderngl as mgl

WIN_SIZE = (1280, 720)

FIXED_UPDATE_RATE = 50


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

        self.grab_mouse_inside_bounded_window = False

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

        # Client
        self.network = network_m.Network()

        # Game State Machine
        self.gsm = gsm_m.GSM(self)

        self.gsm.network = self.network

        # Other
        self.fixed_delta_time = 1 / FIXED_UPDATE_RATE

        self.user_data = data_manager_m.DataManager.load_user_data("Data/UserData.json")

        # self.network.connect()

        # self.gsm.set_state("Debug")

        # self.gsm.set_state("Connection")

        self.gsm.set_state("Menu")

        self.running = True

    def process_window_resize(self, event):
        self.win_size = glm.vec2(event.size)
        pg.display.set_mode((self.win_size.x, self.win_size.y), flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        self.gui.process_window_resize(self.win_size)
        self.gsm.state.process_window_resize(self.win_size)
        self.ctx.viewport = (0, 0, self.win_size.x, self.win_size.y)

    def update_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def before_exit(self, pressed_escape):
        self.gsm.state.before_exit(pressed_escape)

    def get_fps(self):
        return round(self.clock.get_fps())

    def set_mouse_grab(self, value):
        if pg:
            pg.event.set_grab(value)
        self.grab_mouse_inside_bounded_window = False

    @staticmethod
    def set_mouse_visible(value):
        pg.mouse.set_visible(value)

    def exit(self):
        if self.network.id != -1:
            self.network.disconnect()
        input_manager_m.InputManager.release()
        self.gsm.state.exit()
        pg.quit()
        sys.exit()

    def run(self):
        """Main game loop."""
        try:
            accumulated_time = 0
            while self.running:
                accumulated_time += self.delta_time

                # Fixed Update
                while accumulated_time >= self.fixed_delta_time:
                    self.gsm.state.fixed_update()
                    accumulated_time -= self.fixed_delta_time

                # Input Events
                input_manager_m.InputManager.process()

                # Game Logic
                self.gsm.state.update()

                # Scene Rendering
                self.gsm.state.render_level()

                # Gizmo Rendering
                self.gsm.state.render_gizmo()

                # GUI Rendering
                self.gsm.state.render_gui()

                pg.display.flip()

                self.delta_time = self.clock.tick(120) / 1000
                # print("dt: ", self.delta_time)
                # print("time: ", self.time)
                # self.update_time()
                self.time += self.delta_time
        except KeyboardInterrupt:
            self.running = False
            if self.network.id != -1:
                self.network.disconnect()


if __name__ == '__main__':
    app = TeeworldsEngine()
    app.run()
