import Scripts.Source.Abstract.FSM.fsm as fsm_m

import Scripts.Source.GUI.Menu.MenuSM.States.menu_welcome as menu_welcome_m
import Scripts.Source.GUI.Menu.MenuSM.States.menu_play as menu_play_m
import Scripts.Source.GUI.Menu.MenuSM.States.menu_editor as menu_editor_m
import Scripts.Source.GUI.Menu.MenuSM.States.menu_settings as menu_settings_m


class MenuSM(fsm_m.FSM):
    def __init__(self, app, gsm):
        super().__init__()
        self.app = app
        self.gui = app.gui
        self.add_state(menu_welcome_m.MenuWelcome.NAME, menu_welcome_m.MenuWelcome(self))
        self.add_state(menu_play_m.MenuPlay.NAME, menu_play_m.MenuPlay(self, gsm))
        self.add_state(menu_editor_m.MenuEditor.NAME, menu_editor_m.MenuEditor(self, gsm))
        self.add_state(menu_settings_m.MenuSettings.NAME, menu_settings_m.MenuSettings(self, gsm))
        self.set_state(menu_welcome_m.MenuWelcome.NAME)
        # self.set_state(menu_settings_m.MenuSettings.NAME)

        pass

    def release(self):
        super().release()
        self.app = None
        self.canvas = None
