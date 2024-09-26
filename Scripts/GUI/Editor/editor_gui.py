import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.Elements.elements as elements
import Scripts.GUI.Editor.header as header_m
import Scripts.GUI.Editor.hierarchy as hierarchy_m
import Scripts.Source.General.Managers.data_manager as data_manager_m
import glm
import easygui

#  HEADER_BOTTOM                             LEFT_INSPECTOR_CORNER
#    |                                                0.75
#    |   ############################################################
#    ↓   #                    Header                   #            #
#   0.95 ###############################################            #
#        #                                             #            #
#        #                                             #            #
#        #                                             # Inspector  #
#        #                                             #            #
#        #                                             #            #
#        #                                             #            #
#        #                                             ############## 0.5  DIVISION_BETWEEN_INSPECTOR_AND_HIERARCHY
#        #                                             #            #
#        #                                             #            #
#        #                                             #            #
#        #                                             #            #
#        #                                             # Hierarchy  #
#        #                                             #            #
#        #                                             #            #
#        #                                       (G)   #            #
#        #                                             #            #
#        ############################################################
#                                                     0.75
#                                              LEFT_INSPECTOR_CORNER
# G - Gizmo

# def draw_box(w, h):
#     print("#"*w)
#     for i in range(h-2):
#         print("#" + " "*(w-2) + "#")
#     print("#"*w)


# Settings
DEV_MODE = True

Pivot = element_m.Pivot


class EditorGUI:
    HEADER_BOTTOM = 0.95
    LEFT_INSPECTOR_CORNER = 0.75
    DIVISION_BETWEEN_INSPECTOR_AND_HIERARCHY = 0.5

    def __init__(self, editor, win_size, gui):
        self.editor = editor
        self.win_size = glm.vec2(win_size)
        self.aspect_ratio = win_size[0] / win_size[1]
        self.gui = gui
        self.header = header_m.Header(self.gui, self, gui.canvas)
        # self.inspector = inspector_m.Inspector(self, self.main_block)
        self.hierarchy = hierarchy_m.Hierarchy(self.gui, self, gui.canvas)

        self.ask_save_file_before_exit_window = None

    @property
    def windows(self):
        return self.gui.windows

    def update_data_in_hierarchy(self):
        self.hierarchy.update_content()

    def select_element_in_hierarchy(self, object_id):
        self.hierarchy.select_element_in_hierarchy(object_id)

    def unselect_data_in_hierarchy(self):
        self.hierarchy.unselect_all_elements_in_content()

    def ask_save_file_before_exit(self):
        if self.ask_save_file_before_exit_window:
            self.ask_save_file_before_exit_window.position.relative.center = glm.vec2(0.85)
            self.ask_save_file_before_exit_window.update_position()
            return
        window = elements.Window(f"Ask_save_or_not_window_{len(self.gui.windows)}", self.gui.canvas,
                                 self.win_size,
                                 self.gui, "Warning")
        self.ask_save_file_before_exit_window = window
        window.position.relative_window.size = glm.vec2(0.2, 0.15)
        window.position.relative_window.center = glm.vec2(0.85)
        window.position.evaluate_values_by_relative_window()
        window.init()

        hint_text = elements.Text(f"Save scene before exit?", window.inner_data_block, self.win_size,
                                  f"Save scene before exit?",
                                  font_size=1)
        hint_text.color = glm.vec4(0.1, 0.1, 0.1, 1)
        hint_text.pivot = Pivot.Center
        hint_text.position.relative.center = glm.vec2(0.5, 0.8)
        hint_text.update_position()

        def Save(button, gui, pos):
            file_path = easygui.fileopenbox(title='Save', filetypes='\\*.json')
            if file_path:
                if file_path.endswith(".json"):
                    data_manager_m.DataManager.save_scene(gui.editor.level, file_path)
                    # what to do?
                    self.editor.close_app()
                else:
                    window = elements.Window(f"Error_saving_file_window{len(gui.windows)}", self.main_block,
                                             gui.win_size,
                                             self.gui, "Error")
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
                    self.windows.append(window)

        button_apply = elements.Button("Save", window.inner_data_block, self.win_size, self, 'Save', 1.5,
                                       Save,
                                       color=glm.vec4(0, 0.8, 0.1, 1), text_color=glm.vec4(1))
        button_apply.position.relative.center = glm.vec2(0.65, 0.15)
        button_apply.position.relative.size = glm.vec2(0.3)
        button_apply.update_position()

        def no_save_action(button, gui, pos):
            self.editor.close_app()

        button_clear = elements.Button("Exit", window.inner_data_block, self.win_size, self, 'Exit', 1.5,
                                       no_save_action,
                                       color=glm.vec4(0.8, 0.1, 0.1, 1), text_color=glm.vec4(1))
        button_clear.position.relative.center = glm.vec2(0.05, 0.15)
        button_clear.position.relative.size = glm.vec2(0.3)
        button_clear.update_position()

        temp = window.close

        def _extension_to_close():
            self.ask_save_file_before_exit_window = None
            temp()

        window.close = _extension_to_close

        window.update_position()

        self.windows.append(window)

    def process_window_resize(self, new_size):
        self.win_size = new_size

    def delete(self):
        self.editor = None
        self.main_block = None
        self.header = None
        # self.inspector = None
        self.hierarchy = None
        self.ask_save_file_before_exit_window = None
