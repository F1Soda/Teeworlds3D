import Scripts.Source.General.GSM.game_state as state_m

class Game(state_m.GameState):
    NAME = "Game"
    def __init__(self, gsm, app):
        super().__init__(gsm, app)

    def enter(self, params=None):
        ...

    def exit(self):
        ...

    def update(self):
        ...

    def process_window_resize(self, new_size):
        ...
