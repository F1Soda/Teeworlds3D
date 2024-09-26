import Scripts.Source.Abstract.FSM.state as state_m


class FSM:
    def __init__(self):
        self.state = None

        self._states = {}

    def add_state(self, name: str, state: state_m.State):
        self._states[name] = state

    def set_state(self, name, params=None):
        new_state = self._states.get(name)

        if new_state is None:
            print("ERROR: Unknown state")
            return

        if self.state is not None and new_state.NAME == self.state.NAME:
            print(
                f"WARNING: Transition to the same state: {self.state.NAME} -> {self.state.NAME}")
            return

        if self.state is not None:
            self.state.exit()

        self.state = new_state

        self.state.enter(params)

    def release(self):
        self.state = None
        for state in self._states.values():
            state.release()