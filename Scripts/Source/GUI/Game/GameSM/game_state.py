import Scripts.Source.Abstract.FSM.state as state_m


class GameState(state_m.State):
    def __init__(self, game_sm):
        super().__init__(game_sm)
        self.elements = []

    def before_exit(self):
        ...

    def exit(self):
        for element in self.elements:
            element.active = False

    def enter(self, params=None):
        for element in self.elements:
            element.active = True
