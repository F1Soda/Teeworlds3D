import Scripts.Source.Abstract.FSM.fsm as fsm_m

import Scripts.Source.GUI.Game.GameSM.States.game_play as game_play_m


class GameSM(fsm_m.FSM):
    def __init__(self, app, gsm):
        super().__init__()
        self.app = app
        self.gui = app.gui
        self.add_state(game_play_m.GamePlay.NAME, game_play_m.GamePlay(self, gsm))
        # self.add_state(menu_play_m.MenuPlay.NAME, menu_play_m.MenuPlay(self, gsm))
        # self.add_state(menu_editor_m.MenuEditor.NAME, menu_editor_m.MenuEditor(self, gsm))
        self.set_state(game_play_m.GamePlay.NAME)

    def release(self):
        super().release()
        self.app = None
