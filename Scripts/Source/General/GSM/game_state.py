import Scripts.Source.Abstract.FSM.state as state_m


class GameState(state_m.State):
    def __init__(self, gsm, app):
        super().__init__(gsm)
        self.app = app

    def process_window_resize(self, new_size):
        ...

    def fixed_update(self):
        ...

    def render_level(self):
        ...

    def render_gizmo(self):
        ...

    def render_gui(self):
        ...

    def before_exit(self):
        ...

    def release(self):
        super().release()
        self.app = None
