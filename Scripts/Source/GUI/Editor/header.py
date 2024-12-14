import Scripts.Source.GUI.Elements.element as element_m
import Scripts.Source.GUI.Elements.elements as elements
import Scripts.Source.General.utils as utils_m
import Scripts.Source.General.Managers.data_manager as data_manager_m
import copy
import glm
import easygui


class Header(element_m.Element):
    def __init__(self, gui, editor_gui, main_block):
        super().__init__('Header', main_block, gui.win_size)
        self.gui = gui
        self.editor_gui = editor_gui
        self.main_block = main_block

        self.position.relative.left_bottom = glm.vec2(0, editor_gui.HEADER_BOTTOM)
        self.position.relative.right_top = glm.vec2(editor_gui.LEFT_INSPECTOR_CORNER, 1)

        background = elements.Block("Background", self, self.win_size, color=(0.5, 0.5, 0.7, 0.7))
        background.position.relative.right_top = glm.vec2(1)
        self.update_position()

        self.text_header = elements.Text("Header Text", background, self.win_size,
                                         "3D Editor",
                                         font_size=2,
                                         space_between=0.1,
                                         pivot=element_m.Pivot.Center
                                         )
        self.text_header.position.relative.center = glm.vec2(0.5, 0.5)

        rlb = glm.vec2(0.005, 0.1)
        rrt = glm.vec2(0.05, 1 - 0.1)

        def save_action(button, gui, pos):
            file_path = self.gui.app.gsm.state.file_path_level
            if file_path is None:
                file_path = easygui.fileopenbox(title='Save', filetypes='\\*.json')
            if file_path:
                if file_path.endswith(".json"):
                    data_manager_m.DataManager.save_scene(editor_gui.app.level, file_path)
                    return True
                else:
                    window = elements.Window(f"Error_saving_file_window{len(self.gui.windows)}", self.main_block,
                                             gui.win_size,
                                             gui, "Error")
                    window.position.relative_window.size = glm.vec2(0.2, 0.1)
                    window.position.relative_window.center = glm.vec2(0.5)
                    window.position.evaluate_values_by_relative_window()
                    window.init()

                    hint_text = elements.Text(f"Incorrect format selected", window.inner_data_block, self.win_size,
                                              f"Incorrect format selected",
                                              font_size=1)
                    hint_text.color = glm.vec4(0.1, 0.1, 0.1, 1)
                    hint_text.pivot = element_m.Pivot.Center
                    hint_text.position.relative.center = glm.vec2(0.5)
                    hint_text.update_position()

                    window.update_position()
                    self.gui.windows.append(window)

            return False

        save_button = elements.Button("Save Button", background, self.win_size, self.gui,
                                      "Save",
                                      action=save_action,
                                      color=glm.vec4(0, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=1
                                      )
        save_button.position.relative.left_bottom = copy.copy(rlb)
        save_button.position.relative.right_top = copy.copy(rrt)

        rlb = rlb + glm.vec2(rrt.x + rlb.x, 0)
        rrt = rrt + glm.vec2(rrt.x, 0)

        self.ask_save_file_before_load_window = None

        def load_button(button, gui, pos):
            if self.ask_save_file_before_load_window:
                self.ask_save_file_before_load_window.position.relative.center = glm.vec2(0.15, 0.85)
                self.ask_save_file_before_load_window.update_position()
                return

            window = elements.Window(f"Ask_save_or_not_window_{len(self.gui.windows)}", self.main_block,
                                     self.win_size,
                                     self.gui, "Warning")
            self.ask_save_file_before_load_window = window
            window.position.relative_window.size = glm.vec2(0.2, 0.15)
            window.position.relative_window.center = glm.vec2(0.15, 0.85)
            window.position.evaluate_values_by_relative_window()
            window.init()

            hint_text = elements.Text(f"Save scene before load?", window.inner_data_block, self.win_size,
                                      f"Save scene before load?",
                                      font_size=1)
            hint_text.color = glm.vec4(0.1, 0.1, 0.1, 1)
            hint_text.pivot = element_m.Pivot.Center
            hint_text.position.relative.center = glm.vec2(0.5, 0.8)
            hint_text.update_position()

            def load(button, gui, pos):
                file_path = easygui.fileopenbox(title='Load', filetypes='\\*.json')
                if file_path:
                    self.editor_gui.app.load_level(file_path)
                    self.ask_save_file_before_load_window.close()

            def save(button, gui, pos):
                if save_action(button, gui, pos):
                    load(button, gui, pos)

            button_apply = elements.Button("Save", window.inner_data_block, self.win_size, self.gui, 'Save', 1.5,
                                           save,
                                           color=glm.vec4(0, 0.8, 0.1, 1), text_color=glm.vec4(1))
            button_apply.position.relative.center = glm.vec2(0.65, 0.15)
            button_apply.position.relative.size = glm.vec2(0.3)
            button_apply.update_position()

            button_clear = elements.Button("Skip", window.inner_data_block, self.win_size, self.gui, 'Skip', 1.5,
                                           load,
                                           color=glm.vec4(0.8, 0.1, 0.1, 1), text_color=glm.vec4(1))
            button_clear.position.relative.center = glm.vec2(0.05, 0.15)
            button_clear.position.relative.size = glm.vec2(0.3)
            button_clear.update_position()

            temp = window.close

            def _extension_to_close():
                self.ask_save_file_before_load_window = None
                temp()

            window.close = _extension_to_close

            window.update_position()

            self.gui.windows.append(window)

        load_button = elements.Button("Load Button", background, self.win_size, self.gui,
                                      "Load",
                                      action=load_button,
                                      color=glm.vec4(0.7, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=1
                                      )
        load_button.position.relative.left_bottom = copy.copy(rlb)
        load_button.position.relative.right_top = copy.copy(rrt)
        load_button.position.evaluate_values_by_relative()


        def render_mode_button_action(button, gui, pos):
            if button.button_text == "Lines: Off":
                button.button_text = "Lines: On"
            elif button.button_text == "Lines: On":
                button.button_text = "Lines: On(Dashed)"
            elif button.button_text == "Lines: On(Dashed)":
                button.button_text = "Lines: Both"
            elif button.button_text == "Lines: Both":
                button.button_text = "Lines: Off"

            button.update_position()
            editor_gui.app.level.change_hidden_line_mode()

        render_mode_button = elements.Button("Render Mode Button", background, self.win_size, self.gui,
                                             "Lines: Off",
                                             action=render_mode_button_action,
                                             color=glm.vec4(0.1, 0.2, 0.6, 1),
                                             text_color=glm.vec4(1, 1, 1, 1),
                                             text_size=2
                                             )

        render_mode_button.position.relative.size = glm.vec2(0.27, 0.8)
        render_mode_button.position.relative.center = glm.vec2(0.25, 0.5)
        render_mode_button.position.evaluate_values_by_relative()

        def grid_off_on_action(button, gui, pos):
            button.button_text = "Grid: ON" if button.button_text == "Grid: OFF" else "Grid: OFF"
            editor_gui.app.gizmos.draw_grid_and_center_system = not editor_gui.app.gizmos.draw_grid_and_center_system
            pass

        grid_on_off_button = elements.Button("Grid off on button", background, self.win_size, self.gui,
                                             "Grid: ON",
                                             action=grid_off_on_action,
                                             color=glm.vec4(0.0, 0.7, 0.7, 1),
                                             text_color=glm.vec4(1, 1, 1, 1),
                                             text_size=2
                                             )

        grid_on_off_button.position.relative.size = glm.vec2(0.15, 0.8)
        grid_on_off_button.position.relative.center = glm.vec2(0.92, 0.5)
        grid_on_off_button.position.evaluate_values_by_relative()

        self.update_position()

    def render(self):
        if self.text_header:
            utils_m.rainbow_color(self.editor_gui.app.time, self.text_header.color)
        super().render()

    def delete(self):
        self.gui = None
        self.main_block = None
        self.text_header = None
        self.ask_save_file_before_load_window = None
        super().delete()
