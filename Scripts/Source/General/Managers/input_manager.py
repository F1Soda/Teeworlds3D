import pygame as pg

import Scripts.Source.General.utils as utils_m
import enum
import glm


class MouseButtonState(enum.Enum):
    Idle = 0
    Pressed = 1
    Hold = 2
    Released = 3


class InputManager:
    # Mouse
    mouse_states = [MouseButtonState.Idle, MouseButtonState.Idle, MouseButtonState.Idle]
    past_mouse_buttons = (False, False, False)
    mouse_position = glm.vec2(0, 0)
    mouse_diff = (0, 0)
    keys = {}
    pressed_keyboard_char = None

    handle_left_click_event = utils_m.PriorityEventDelegate()
    handle_left_hold_event = utils_m.PriorityEventDelegate()
    handle_left_release_event = utils_m.PriorityEventDelegate()
    handle_right_click_event = utils_m.PriorityEventDelegate()
    handle_right_hold_event = utils_m.PriorityEventDelegate()
    handle_right_release_event = utils_m.PriorityEventDelegate()

    handle_keyboard_press = utils_m.PriorityEventDelegate()

    # Other
    _app = None

    @staticmethod
    def init(app):
        InputManager._app = app

    @staticmethod
    def update_mouse_status():
        mouse_buttons = pg.mouse.get_pressed()

        for i in range(3):
            if mouse_buttons[i]:
                if InputManager.mouse_states[i] == MouseButtonState.Idle:
                    InputManager.mouse_states[i] = MouseButtonState.Pressed
                elif InputManager.mouse_states[i] == MouseButtonState.Pressed:
                    InputManager.mouse_states[i] = MouseButtonState.Hold
            if not mouse_buttons[i]:
                if InputManager.past_mouse_buttons[i]:
                    InputManager.mouse_states[i] = MouseButtonState.Released
                else:
                    InputManager.mouse_states[i] = MouseButtonState.Idle

        InputManager.past_mouse_buttons = mouse_buttons
        InputManager.mouse_position = glm.vec2(pg.mouse.get_pos())
        InputManager.mouse_position.y = InputManager._app.win_size.y - InputManager.mouse_position.y

    @staticmethod
    def process():
        InputManager.update_mouse_status()
        InputManager.keys = pg.key.get_pressed()
        InputManager.pressed_keyboard_char = None

        InputManager.mouse_diff = pg.mouse.get_rel()
        if InputManager._app.grab_mouse_inside_bounded_window:
            m_pos = InputManager.mouse_position
            win_size = InputManager._app.win_size
            if m_pos.x > win_size.x - 100 or m_pos.x < 100 or m_pos.y > win_size.y - 100 or m_pos.y < 100:
                pg.mouse.set_pos(InputManager._app.win_size.x // 2, InputManager._app.win_size.y // 2)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                InputManager._app.before_exit(False)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                InputManager._app.before_exit(True)
            elif event.type == pg.VIDEORESIZE:
                InputManager._app.process_window_resize(event)
            elif event.type == pg.KEYDOWN:
                if event.unicode == "G":
                    if InputManager._app.gsm.state.NAME == "Editor":
                        InputManager._app.gsm.state.draw_gui = not InputManager._app.gsm.state.draw_gui
                if event.unicode.isalnum() and event.unicode.isascii():
                    InputManager.pressed_keyboard_char = event.unicode
                elif event.unicode == " ":
                    InputManager.pressed_keyboard_char = " "
                elif event.unicode == ".":
                    InputManager.pressed_keyboard_char = "."
                elif event.unicode == ",":
                    InputManager.pressed_keyboard_char = ","
                elif event.unicode == "?":
                    InputManager.pressed_keyboard_char = "?"

        InputManager.handle_keyboard_press(InputManager.keys, InputManager.pressed_keyboard_char)

        mouse_pos = InputManager.mouse_position
        mouse_states = InputManager.mouse_states

        if mouse_states[0] == MouseButtonState.Pressed:
            InputManager.handle_left_click_event(mouse_pos)

        if mouse_states[0] == MouseButtonState.Hold:
            InputManager.handle_left_hold_event(mouse_pos)

        if mouse_states[0] == MouseButtonState.Released:
            InputManager.handle_left_release_event(mouse_pos)

        if mouse_states[2] == MouseButtonState.Pressed:
            InputManager.handle_right_click_event(mouse_pos)

        if mouse_states[2] == MouseButtonState.Hold:
            InputManager.handle_right_hold_event(mouse_pos)

        if mouse_states[2] == MouseButtonState.Released:
            InputManager.handle_right_release_event(mouse_pos)

    @staticmethod
    def release():
        InputManager.handle_keyboard_press.delete()
        InputManager.handle_left_click_event.delete()
        InputManager.handle_left_hold_event.delete()
        InputManager.handle_left_release_event.delete()
        InputManager.handle_right_click_event.delete()
        InputManager.handle_right_hold_event.delete()
        InputManager.handle_right_release_event.delete()
