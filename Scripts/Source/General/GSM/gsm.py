import Scripts.Source.General.GSM.game_state as state_m
import Scripts.Source.General.GSM.menu as menu_m
import Scripts.Source.General.GSM.editor as editor_m
import Scripts.Source.General.GSM.game as game_m
import Scripts.Source.Abstract.FSM.fsm as fsm_m


class GSM(fsm_m.FSM):
    def __init__(self, app):
        self.app = app
        super().__init__()

        self.state = None  # type: state_m.GameState

        self.add_state(menu_m.Menu.NAME, menu_m.Menu(app, self))
        self.add_state(editor_m.Editor.NAME, editor_m.Editor(app, self))
        self.add_state(game_m.Game.NAME, game_m.Game(app, self))

        self.set_state("Menu")
