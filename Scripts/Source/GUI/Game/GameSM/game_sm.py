import Scripts.Source.Abstract.FSM.fsm as fsm_m

import Scripts.Source.GUI.Game.GameSM.States.game_play as game_play_m
import Scripts.Source.GUI.Game.GameSM.States.game_died as game_died_m


class GameSM(fsm_m.FSM):
    def __init__(self, app, gsm):
        super().__init__()
        self.app = app
        self.gui = app.gui
        self.add_state(game_play_m.GamePlay.NAME, game_play_m.GamePlay(self, gsm))
        self.add_state(game_died_m.GameDied.NAME, game_died_m.GameDied(self, gsm))
        self.set_state(game_play_m.GamePlay.NAME)

    def update(self):
        self.state.update()

    def release(self):
        super().release()
        self.app = None
