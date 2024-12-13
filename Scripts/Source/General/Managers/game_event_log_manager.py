class GameEventLogManager:
    def __init__(self, game_play_state, max_size=5):
        self.messages = []
        self.max_size = max_size
        self.game_play_state = game_play_state

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > self.max_size:
            self.messages.pop(0)
        self.update_gui()

    def clear(self):
        self.messages.clear()
        self.update_gui()

    def update_gui(self):
        self.game_play_state.set_game_event_log(self.get_log())

    def get_log(self):
        log = ""
        for message in self.messages[::-1]:
            log += message + "\n"
        return log

    def delete(self):
        self.messages.clear()
        self.game_event_log = None
