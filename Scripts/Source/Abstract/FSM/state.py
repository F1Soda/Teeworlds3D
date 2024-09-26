class State:
    NAME = "GameState"

    def __init__(self, fsm):
        self.fsm = fsm

    def enter(self, params=None):
        ...

    def exit(self):
        ...

    def update(self):
        ...

    def release(self):
        self.fsm = None