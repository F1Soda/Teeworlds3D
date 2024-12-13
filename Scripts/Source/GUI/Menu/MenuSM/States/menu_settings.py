import Scripts.Source.GUI.Menu.MenuSM.menu_state as menu_state_m
import Scripts.Source.GUI.Elements.elements as elements
import Scripts.Source.GUI.Elements.element as element_m
import Scripts.Source.General.Managers.data_manager as data_manager_m
import glm


class MenuSettings(menu_state_m.MenuState):
    NAME = "SETTINGS"

    def __init__(self, menu_sm, gsm):
        super().__init__(menu_sm)
        win_size = menu_sm.app.win_size
        self.gsm = gsm
        canvas = menu_sm.gui.canvas

        self.selected_level_button = None
        self.selected_level_path = None

        def back_button_action(button, gui, pos):
            self.fsm.set_state("WELCOME")

        back_button = elements.Button("Back Button", canvas, win_size, self,
                                      "<<",
                                      action=back_button_action,
                                      color=glm.vec4(0.7, 0.1, 0.1, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=2
                                      )

        back_button.position.relative.center = glm.vec2(0.03, 0.9)
        back_button.position.relative.size = glm.vec2(0.04, 0.07)
        back_button.position.evaluate_values_by_relative()
        self.elements.append(back_button)

        levels_label = elements.Text("Settings label", canvas, win_size,
                                     "Settings", font_size=3)
        levels_label.pivot = element_m.Pivot.LeftBottom
        levels_label.position.relative.center = glm.vec2(0.15, 0.9)

        levels_label.update_position()
        self.elements.append(levels_label)

        ltp = glm.vec2(0.03, 0.74)

        user_name_label = elements.Text("User Name", canvas, win_size,
                                        "User Name", font_size=2)
        user_name_label.pivot = element_m.Pivot.LeftBottom
        user_name_label.position.relative.left_bottom = ltp.xy
        user_name_label.update_position()
        self.elements.append(user_name_label)

        ltp.y -= user_name_label.position.relative.size.y - 0.02

        self.input_field = elements.input_field_m.InputField("User_name", canvas, win_size, menu_sm.gui)
        self.input_field.position.relative.size = glm.vec2(0.15, 0.05)
        self.input_field.position.relative.left_bottom = glm.vec2(ltp.x, ltp.y - 0.05)
        self.input_field.position.relative.right_top = glm.vec2(ltp.x + 0.15, ltp.y)
        self.input_field.update_position()
        self.input_field.text.text = gsm.app.user_data["user_name"]
        self.input_field.text.position.relative.left_bottom = glm.vec2(0.05,
                                                                       0.5 - self.input_field.text.position.relative.size.y / 2)

        self.elements.append(self.input_field)

        ltp.y -= self.input_field.position.relative.size.y + 0.02

        def save_button_action(button, gui, pos):
            data_manager_m.DataManager.save_user_name("Data/UserData.json", self.input_field.text.text)
            self.gsm.app.user_data["user_name"] = self.input_field.text.text

        save_button = elements.Button("Save Button", canvas, win_size, self,
                                      "Save",
                                      action=save_button_action,
                                      color=glm.vec4(0.7, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=2
                                      )
        save_button.position.relative.left_bottom = glm.vec2(ltp.x, ltp.y - 0.05)
        save_button.position.relative.size = glm.vec2(0.2, 0.05)
        save_button.position.evaluate_values_by_relative()
        self.elements.append(save_button)

        self.exit()

        canvas.update_position()
