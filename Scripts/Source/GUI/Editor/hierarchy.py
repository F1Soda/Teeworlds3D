import Scripts.Source.GUI.Elements.element as element_m
import Scripts.Source.GUI.Elements.elements as elements
import Scripts.Source.General.Managers.object_picker as object_picker_m
import Scripts.Source.General.Managers.object_creator as object_creator_m
import Scripts.Source.General.Managers.input_manager as input_manager_m
import Scripts.Source.General.utils as utils_m
import pygame as pg
import glm
import re

Pivot = element_m.Pivot


class Hierarchy(element_m.Element):
    def __init__(self, gui, editor_gui, main_block):
        super().__init__('Header', main_block, gui.win_size)
        self.gui = gui
        self.editor_gui = editor_gui
        self.main_block = main_block
        self.selected_elements = []

        input_manager_m.InputManager.handle_keyboard_press += self._handle_delete_objs

        # Events
        self.select_element = utils_m.EventDelegate()
        self.unselect_element = utils_m.EventDelegate()

        self.position.relative.left_bottom = glm.vec2(editor_gui.LEFT_INSPECTOR_CORNER, 0)
        self.position.relative.right_top = glm.vec2(1)

        background = elements.Block("Background", self, self.win_size, color=(0.3, 0.1, 0.1, 0.5))
        background.position.relative.right_top = glm.vec2(1)
        self.update_position()

        text_header = elements.Text("Header Text", background, self.win_size,
                                    "Hierarchy",
                                    centered_x=True,
                                    centered_y=True,
                                    font_size=2,
                                    space_between=0.1,
                                    pivot=Pivot.Center
                                    )
        text_header.position.relative.center = glm.vec2(0.5, 0.975)
        text_header.update_position()

        def custom_right_click_handle(pos: glm.vec2):
            self.sub_menu.active = True
            if pos.y / self.gui.win_size.y > 0.7:
                self.sub_menu.position.absolute.center = glm.vec2(
                    pos.x - self.sub_menu.position.absolute.size.x / 2,
                    pos.y - self.sub_menu.position.absolute.size.y / 2
                )
            else:
                self.sub_menu.position.absolute.center = glm.vec2(
                    pos.x - self.sub_menu.position.absolute.size.x / 2,
                    pos.y + self.sub_menu.position.absolute.size.y / 2
                )
            self.sub_menu.position.evaluate_values_by_absolute()
            self.sub_menu.update_position()
            self.gui.active_sub_menu = self.sub_menu
            self.gui.last_clicked_element = self.sub_menu

        def custom_left_click_handle(pos: glm.vec2):
            for selected_elements in self.selected_elements:
                selected_elements[0].color = glm.vec4(0.7, 0.7, 0.7, 1)
            self.selected_elements.clear()
            object_picker_m.ObjectPicker.unselect_object()

        background.handle_right_click = custom_right_click_handle
        background.handle_left_click = custom_left_click_handle

        self.content = elements.Content("Hierarchy_content", background, self.win_size)
        self.content.add_to_bottom = True
        self.content.active = True
        self.content.pivot = Pivot.Top
        self.content.position.relative.center = glm.vec2(0.5, 0.95)
        self.content.position.evaluate_values_by_relative()

        self.sub_menu = None
        self.sub_menu_plane = None
        self.sub_menu_other = None

        self._init_sub_menu()

    def _handle_delete_objs(self, keys, char):
        if keys[pg.K_DELETE]:
            for button, obj_id in self.selected_elements:
                self.gui.app.gsm.state.level.delete_object_by_id(obj_id)

    # def _handle_copy_obj(self, keys, char):
    #     if keys[pg.K_LCTRL] and keys[pg.K_c]:
    #         for button, obj_id in self.selected_elements:
    #             self.gui.app.gsm.state.level.delete_object_by_id(obj_id)

    def _create_element_in_content(self, content, action, text, number):
        content_element = elements.Block(f"Element_{number}_in_content_{content.name}", None, self.win_size,
                                         (1, 1, 1, 0.5))
        content_element.position.relative_window.size = glm.vec2(0.25, 0.03)
        content_element.position.evaluate_values_by_relative_window()

        button = elements.Button(f"{text}_Button", content_element, self.win_size, self.gui,
                                 text,
                                 action=action,
                                 color=glm.vec4(0.7, 0.7, 0.7, 1),
                                 text_size=1
                                 )

        button.position.relative.left_bottom = glm.vec2(0)
        button.position.relative.right_top = glm.vec2(1)
        button.position.evaluate_values_by_relative()
        button.update_position()

        content.add(content_element)
        content.update_position()

    def process_window_resize(self, new_size: glm.vec2):
        super().process_window_resize(new_size)
        self.update_content()


    def _init_sub_menu(self):
        self._init_sub_menu_plane()
        self._init_sub_menu_polyhedrons()
        self._init_sub_menu_other()

        self.sub_menu = elements.Content("Sub Menu", self, self.win_size, (1, 1, 1, 0.5))
        self.sub_menu.position.relative.center = glm.vec2(0.5)
        self.sub_menu.position.evaluate_values_by_relative()

        def create_polyhedrons_button_action(button, gui, pos):
            self.sub_menu_polyhedrons.active = True
            self.sub_menu_polyhedrons.position.absolute.center = glm.vec2(
                pos.x - self.sub_menu_polyhedrons.position.absolute.size.x / 2,
                pos.y + self.sub_menu_polyhedrons.position.absolute.size.y / 2
            )
            self.sub_menu_polyhedrons.position.evaluate_values_by_absolute()
            self.sub_menu_polyhedrons.update_position()
            self.gui.active_sub_menu = self.sub_menu_polyhedrons
            self.gui.last_clicked_element = self.sub_menu_polyhedrons

        self._create_button_in_sub_menu(self.sub_menu, create_polyhedrons_button_action, "Create Polyhedrons", 1)

        def create_plane_button_action(button, gui, pos):
            self.sub_menu_plane.active = True
            self.sub_menu_plane.position.absolute.center = glm.vec2(
                pos.x - self.sub_menu_plane.position.absolute.size.x / 2,
                pos.y + self.sub_menu_plane.position.absolute.size.y / 2
            )
            self.sub_menu_plane.position.evaluate_values_by_absolute()
            self.sub_menu_plane.update_position()
            self.gui.active_sub_menu = self.sub_menu_plane
            self.gui.last_clicked_element = self.sub_menu_plane

        self._create_button_in_sub_menu(self.sub_menu, create_plane_button_action, "Create Plane", 2)

        def create_point_button(button, gui, pos):
            self.editor_gui.app.level.add(object_creator_m.ObjectCreator.create_point(glm.vec4(0, 0.7, 0.1, 1)))

        self._create_button_in_sub_menu(self.sub_menu, create_point_button, "Create Point", 2)

        def create_segment_button(button, gui, pos):
            window = elements.Window(f"Ask_plane_data_window_{len(self.gui.windows)}", self.main_block,
                                     gui.win_size,
                                     gui, "Create Segment")
            window.position.relative_window.size = glm.vec2(0.3, 0.3) / 1.25
            window.position.relative_window.center = glm.vec2(0.5)
            window.position.evaluate_values_by_relative_window()
            window.update_position()

            temp = window.close

            def _extension_close():
                self.select_element -= handle_select_element
                self.unselect_element -= handle_unselect_element
                temp()

            window.close = _extension_close

            hint_text = elements.Text(f"Select points", window.inner_data_block, self.win_size,
                                      f"Select points",
                                      font_size=1.5)
            hint_text.color = glm.vec4(0.1, 0.1, 0.1, 1)
            hint_text.pivot = Pivot.Center
            hint_text.position.relative.center = glm.vec2(0.5, 0.9)
            hint_text.update_position()

            text_point = elements.Text(f"Point 1: ", window.inner_data_block, self.win_size,
                                       f"Point 1: ",
                                       font_size=1.5)
            text_point.color = glm.vec4(0.1, 0.1, 0.1, 1)
            text_point.pivot = Pivot.Center
            text_point.position.relative.center = glm.vec2(0.2, 0.7)
            text_point.update_position()

            input_field_point = elements.InputField(f"input_field_point", window.inner_data_block,
                                                    self.win_size,
                                                    self.gui,
                                                    text_size=1.5)
            input_field_point.position.relative.size = glm.vec2(0.5, 0.15)
            input_field_point.position.relative.center = glm.vec2(0.7, 0.7)
            input_field_point.update_position()
            input_field_point.text.position.relative.left_bottom = glm.vec2(0.05,
                                                                            0.5 - input_field_point.text.position.relative.size.y / 2)
            input_field_point.text.text = ""
            input_field_point.editable = False

            text_point2 = elements.Text(f"Point 2: ", window.inner_data_block, self.win_size,
                                        f"Point 2: ",
                                        font_size=1.5)
            text_point2.color = glm.vec4(0.1, 0.1, 0.1, 1)
            text_point2.pivot = Pivot.Center
            text_point2.position.relative.center = glm.vec2(0.2, 0.5)
            text_point2.update_position()

            input_field_point2 = elements.InputField(f"input_field_point", window.inner_data_block,
                                                     self.win_size,
                                                     self.gui,
                                                     text_size=1.5)
            input_field_point2.position.relative.size = glm.vec2(0.5, 0.15)
            input_field_point2.position.relative.center = glm.vec2(0.7, 0.5)
            input_field_point2.update_position()
            input_field_point2.text.position.relative.left_bottom = glm.vec2(0.05,
                                                                             0.5 - input_field_point2.text.position.relative.size.y / 2)
            input_field_point2.text.text = ""
            input_field_point2.editable = False

            point_component_1 = None
            point_component_2 = None

            def apply(button, gui, pos):
                if point_component_1 is None or point_component_2 is None:
                    return
                p1 = point_component_1.rely_object
                p2 = point_component_2.rely_object
                self.editor_gui.app.level.add(
                    object_creator_m.ObjectCreator.create_segment(glm.vec4(0.7, 0.5, 0.7, 1), p1, p2))
                window.close()

            button_apply = elements.Button("Apply", window.inner_data_block, self.win_size, self.gui, 'Create', 1.5,
                                           apply,
                                           color=glm.vec4(0, 0.8, 0, 1), text_color=glm.vec4(1))
            button_apply.position.relative.center = glm.vec2(0.65, 0.05)
            button_apply.position.relative.size = glm.vec2(0.3, 0.15)
            button_apply.update_position()

            def clear_fields(button, gui, pos):
                nonlocal point_component_1
                nonlocal point_component_2
                point_component_1 = None
                input_field_point.text.text = ""
                point_component_2 = None
                input_field_point2.text.text = ""

            button_clear = elements.Button("Clear", window.inner_data_block, self.win_size, self.gui, 'Clear', 1.5,
                                           clear_fields,
                                           color=glm.vec4(0.8, 0.8, 0, 1), text_color=glm.vec4(1))
            button_clear.position.relative.center = glm.vec2(0.05, 0.05)
            button_clear.position.relative.size = glm.vec2(0.3, 0.15)
            button_clear.update_position()

            window.update_position()

            def handle_select_element(obj_id):
                nonlocal point_component_2
                nonlocal point_component_1
                obj = self.editor_gui.app.level.objects[obj_id]
                point = obj.get_component_by_name("Point")
                if point:
                    if point_component_1 is None:
                        input_field_point.text.text = obj.name
                        point_component_1 = point
                        return
                    if point_component_2 is None:
                        input_field_point2.text.text = obj.name
                        point_component_2 = point
                        return

            def handle_unselect_element(obj_id):
                nonlocal point_component_2
                nonlocal point_component_1
                if obj_id == point_component_1.rely_element.id:
                    point_component_1 = None
                    input_field_point.text.text = ""
                    return
                if obj_id == point_component_2.rely_element.id:
                    point_component_2 = None
                    input_field_point2.text.text = ""
                    return

            self.select_element += handle_select_element
            self.unselect_element += handle_unselect_element

            self.gui.windows.append(window)

        self._create_button_in_sub_menu(self.sub_menu, create_segment_button, "Create Segment", 3)

        def create_other_button(button, gui, pos):
            self.sub_menu_other.active = True
            self.sub_menu_other.position.absolute.center = glm.vec2(
                pos.x - self.sub_menu_other.position.absolute.size.x / 2,
                pos.y + self.sub_menu_other.position.absolute.size.y / 2
            )
            self.sub_menu_other.position.evaluate_values_by_absolute()
            self.sub_menu_other.update_position()
            self.gui.active_sub_menu = self.sub_menu_other
            self.gui.last_clicked_element = self.sub_menu_other

        self._create_button_in_sub_menu(self.sub_menu, create_other_button, "Other", 3)

    def _init_sub_menu_plane(self):
        self.sub_menu_plane = elements.Content("Sub Menu Plane", self, self.win_size,
                                               (1, 1, 1, 0.5))
        self.sub_menu_plane.position.relative.center = glm.vec2(0.5)
        self.sub_menu_plane.position.evaluate_values_by_relative()
        self.sub_menu_plane.active = False

        def create_plane(button, gui, pos):
            self.editor_gui.app.level.add(object_creator_m.ObjectCreator.create_plane('gray_lit'))

        self._create_button_in_sub_menu(self.sub_menu_plane, create_plane, "Plane", 1, 0.2)

        def create_ask_window_element_1(button, gui, pos):
            window = elements.Window(f"Ask_plane_data_window_{len(self.gui.windows)}", self.main_block,
                                     gui.win_size,
                                     gui, "Create plane by 3 point")
            window.position.relative_window.size = glm.vec2(0.3, 0.3) / 1.25
            window.position.relative_window.center = glm.vec2(0.5)
            window.position.evaluate_values_by_relative_window()
            window.init()

            temp = window.close

            def _extension_close():
                self.select_element -= handle_select_element
                self.unselect_element -= handle_unselect_element
                temp()

            window.close = _extension_close

            hint_text = elements.Text(f"Select points", window.inner_data_block, self.win_size,
                                      f"Select points",
                                      font_size=1.5)
            hint_text.color = glm.vec4(0.1, 0.1, 0.1, 1)
            hint_text.pivot = Pivot.Center
            hint_text.position.relative.center = glm.vec2(0.5, 0.9)
            hint_text.update_position()

            text_point_1 = elements.Text(f"Point 1: ", window.inner_data_block, self.win_size,
                                         f"Point 1: ",
                                         font_size=1.5)
            text_point_1.color = glm.vec4(0.1, 0.1, 0.1, 1)
            text_point_1.pivot = Pivot.Center
            text_point_1.position.relative.center = glm.vec2(0.2, 0.7)
            text_point_1.update_position()

            input_field_point_1 = elements.InputField(f"input_field_point_1", window.inner_data_block,
                                                      self.win_size,
                                                      self.gui,
                                                      text_size=1.5)
            input_field_point_1.position.relative.size = glm.vec2(0.5, 0.15)
            input_field_point_1.position.relative.center = glm.vec2(0.7, 0.7)
            input_field_point_1.update_position()
            input_field_point_1.text.position.relative.left_bottom = glm.vec2(0.05,
                                                                              0.5 - input_field_point_1.text.position.relative.size.y / 2)
            input_field_point_1.text.text = ""
            input_field_point_1.editable = False

            text_point_2 = elements.Text(f"Point 2: ", window.inner_data_block, self.win_size,
                                         f"Point 2: ",
                                         font_size=1.5)
            text_point_2.color = glm.vec4(0.1, 0.1, 0.1, 1)
            text_point_2.pivot = Pivot.Center
            text_point_2.position.relative.center = glm.vec2(0.2, 0.5)
            text_point_2.update_position()

            input_field_point_2 = elements.InputField(f"input_field_point_2", window.inner_data_block,
                                                      self.win_size,
                                                      self.gui,
                                                      text_size=1.5)
            input_field_point_2.position.relative.size = glm.vec2(0.5, 0.15)
            input_field_point_2.position.relative.center = glm.vec2(0.7, 0.5)
            input_field_point_2.update_position()
            input_field_point_2.text.position.relative.left_bottom = glm.vec2(0.05,
                                                                              0.5 - input_field_point_2.text.position.relative.size.y / 2)
            input_field_point_2.text.text = ""
            input_field_point_2.editable = False

            text_point_3 = elements.Text(f"Point 3: ", window.inner_data_block, self.win_size,
                                         f"Point 3: ",
                                         font_size=1.5)
            text_point_3.color = glm.vec4(0.1, 0.1, 0.1, 1)
            text_point_3.pivot = Pivot.Center
            text_point_3.position.relative.center = glm.vec2(0.2, 0.3)
            text_point_3.update_position()

            input_field_point_3 = elements.InputField(f"input_field_point_3", window.inner_data_block,
                                                      self.win_size,
                                                      self.gui,
                                                      text_size=1.5)
            input_field_point_3.position.relative.size = glm.vec2(0.5, 0.15)
            input_field_point_3.position.relative.center = glm.vec2(0.7, 0.3)
            input_field_point_3.update_position()
            input_field_point_3.text.position.relative.left_bottom = glm.vec2(0.05,
                                                                              0.5 - input_field_point_3.text.position.relative.size.y / 2)
            input_field_point_3.text.text = ""
            input_field_point_3.editable = False

            p1 = None
            p2 = None
            p3 = None

            def apply(button, gui, pos):
                nonlocal p1
                nonlocal p2
                nonlocal p3
                if p1 is None or p2 is None or p3 is None:
                    return
                self.editor_gui.app.level.add(object_creator_m.ObjectCreator.create_plane_by_3_points(p1, p2, p3))
                window.close()

            button_apply = elements.Button("Apply", window.inner_data_block, self.win_size, self.gui, 'Create', 1.5,
                                           apply,
                                           color=glm.vec4(0, 0.8, 0, 1), text_color=glm.vec4(1))
            button_apply.position.relative.center = glm.vec2(0.65, 0.05)
            button_apply.position.relative.size = glm.vec2(0.3, 0.15)
            button_apply.update_position()

            def clear_fields(button, gui, pos):
                nonlocal p1
                nonlocal p2
                nonlocal p3
                input_field_point_1.text.text = ""
                input_field_point_2.text.text = ""
                input_field_point_3.text.text = ""

            button_clear = elements.Button("Clear", window.inner_data_block, self.win_size, self.gui, 'Clear', 1.5,
                                           clear_fields,
                                           color=glm.vec4(0.8, 0.8, 0, 1), text_color=glm.vec4(1))
            button_clear.position.relative.center = glm.vec2(0.05, 0.05)
            button_clear.position.relative.size = glm.vec2(0.3, 0.15)
            button_clear.update_position()

            window.update_position()

            def handle_select_element(obj_id):
                nonlocal p1
                nonlocal p2
                nonlocal p3
                obj = self.editor_gui.app.level.objects[obj_id]
                point = obj.get_component_by_name("Point")
                if point:
                    i = len(self.selected_elements)
                    if i == 0:
                        input_field_point_1.text.text = obj.name
                        p1 = obj
                    elif i == 1:
                        input_field_point_2.text.text = obj.name
                        p2 = obj
                    elif i == 2:
                        input_field_point_3.text.text = obj.name
                        p3 = obj

            def handle_unselect_element(obj_id):
                nonlocal p1
                nonlocal p2
                nonlocal p3
                obj = self.editor_gui.app.level.objects[obj_id]
                point = obj.get_component_by_name("Point")
                if point:
                    i = len(self.selected_elements)
                    if i == 1:
                        input_field_point_1.text.text = ""
                        p1 = None
                    elif i == 2:
                        input_field_point_2.text.text = ""
                        p2 = None
                    elif i == 3:
                        input_field_point_3.text.text = ""
                        p3 = None

            self.select_element += handle_select_element
            self.unselect_element += handle_unselect_element

            self.gui.windows.append(window)

        def create_ask_window_element_2(button, gui, pos):
            window = elements.Window(f"Ask_plane_data_window_{len(self.gui.windows)}", self.main_block,
                                     gui.win_size,
                                     gui, "Enter data")
            window.position.relative_window.size = glm.vec2(0.3, 0.3) / 1.25
            window.position.relative_window.center = glm.vec2(0.5)
            window.position.evaluate_values_by_relative_window()
            window.init()

            temp = window.close

            def _extension_close():
                self.select_element -= handle_select_element
                self.unselect_element -= handle_unselect_element
                temp()

            window.close = _extension_close

            hint_text = elements.Text(f"Select point and segment", window.inner_data_block, self.win_size,
                                      f"Select point and segment",
                                      font_size=1.5)
            hint_text.color = glm.vec4(0.1, 0.1, 0.1, 1)
            hint_text.pivot = Pivot.Center
            hint_text.position.relative.center = glm.vec2(0.5, 0.9)
            hint_text.update_position()

            text_point = elements.Text(f"Point: ", window.inner_data_block, self.win_size,
                                       f"Point: ",
                                       font_size=1.5)
            text_point.color = glm.vec4(0.1, 0.1, 0.1, 1)
            text_point.pivot = Pivot.Center
            text_point.position.relative.center = glm.vec2(0.2, 0.7)
            text_point.update_position()

            input_field_point = elements.InputField(f"input_field_point", window.inner_data_block,
                                                    self.win_size,
                                                    self.gui,
                                                    text_size=1.5)
            input_field_point.position.relative.size = glm.vec2(0.5, 0.15)
            input_field_point.position.relative.center = glm.vec2(0.7, 0.7)
            input_field_point.update_position()
            input_field_point.text.position.relative.left_bottom = glm.vec2(0.05,
                                                                            0.5 - input_field_point.text.position.relative.size.y / 2)
            input_field_point.text.text = ""
            input_field_point.editable = False

            text_segment = elements.Text(f"Segment: ", window.inner_data_block, self.win_size,
                                         f"Segment: ",
                                         font_size=1.5)
            text_segment.color = glm.vec4(0.1, 0.1, 0.1, 1)
            text_segment.pivot = Pivot.Center
            text_segment.position.relative.center = glm.vec2(0.2, 0.5)
            text_segment.update_position()

            input_field_segment = elements.InputField(f"input_field_segment", window.inner_data_block,
                                                      self.win_size,
                                                      self.gui,
                                                      text_size=1.5)
            input_field_segment.position.relative.size = glm.vec2(0.5, 0.15)
            input_field_segment.position.relative.center = glm.vec2(0.7, 0.5)
            input_field_segment.update_position()
            input_field_segment.text.position.relative.left_bottom = glm.vec2(0.05,
                                                                              0.5 - input_field_segment.text.position.relative.size.y / 2)
            input_field_segment.text.text = ""
            input_field_segment.editable = False

            point_component = None
            segment_component = None

            def apply(button, gui, pos):
                if point_component is None or segment_component is None:
                    return
                p1 = point_component.rely_object
                p2 = segment_component.gizmos_segment.p1
                p3 = segment_component.gizmos_segment.p2
                plane = object_creator_m.ObjectCreator.create_plane_by_3_points(p1, p2, p3)
                self.editor_gui.app.level.objects[plane.id] = plane
                self.update_content()
                window.close()

            button_apply = elements.Button("Apply", window.inner_data_block, self.win_size, self.gui, 'Create', 1.5,
                                           apply,
                                           color=glm.vec4(0, 0.8, 0, 1), text_color=glm.vec4(1))
            button_apply.position.relative.center = glm.vec2(0.65, 0.05)
            button_apply.position.relative.size = glm.vec2(0.3, 0.15)
            button_apply.update_position()

            def clear_fields(button, gui, pos):
                point_component = None
                input_field_point.text.text = ""
                segment_component = None
                input_field_point.text.text = ""

            button_clear = elements.Button("Clear", window.inner_data_block, self.win_size, self.gui, 'Clear', 1.5,
                                           clear_fields,
                                           color=glm.vec4(0.8, 0.8, 0, 1), text_color=glm.vec4(1))
            button_clear.position.relative.center = glm.vec2(0.05, 0.05)
            button_clear.position.relative.size = glm.vec2(0.3, 0.15)
            button_clear.update_position()

            window.update_position()

            def handle_select_element(obj_id):
                nonlocal segment_component
                nonlocal point_component
                obj = self.editor_gui.app.level.objects[obj_id]
                point = obj.get_component_by_name("Point")
                if point:
                    input_field_point.text.text = obj.name
                    point_component = point
                    return
                segment = obj.get_component_by_name("Segment")
                if segment:
                    input_field_segment.text.text = obj.name
                    segment_component = segment
                    return

            def handle_unselect_element(obj_id):
                nonlocal segment_component
                nonlocal point_component
                if obj_id == point_component.rely_element.id:
                    point_component = None
                    input_field_point.text.text = ""
                    return
                if obj_id == segment_component.rely_element.id:
                    segment_component = None
                    input_field_point.text.text = ""
                    return

            self.select_element += handle_select_element
            self.unselect_element += handle_unselect_element

            self.gui.windows.append(window)

        def create_ask_window_element_3(button, gui, pos):
            window = elements.Window(f"Ask_plane_data_window_{len(self.gui.windows)}", self.main_block,
                                     gui.win_size,
                                     gui, "Enter data")
            window.position.relative_window.size = glm.vec2(0.3, 0.3) / 1.25
            window.position.relative_window.center = glm.vec2(0.5)
            window.position.evaluate_values_by_relative_window()
            window.init()

            temp = window.close

            def _extension_close():
                self.select_element -= handle_select_element
                self.unselect_element -= handle_unselect_element
                temp()

            window.close = _extension_close

            hint_text = elements.Text(f"Select point and plane", window.inner_data_block, self.win_size,
                                      f"Select point and plane",
                                      font_size=1.5)
            hint_text.color = glm.vec4(0.1, 0.1, 0.1, 1)
            hint_text.pivot = Pivot.Center
            hint_text.position.relative.center = glm.vec2(0.5, 0.9)
            hint_text.update_position()

            text_point = elements.Text(f"Point: ", window.inner_data_block, self.win_size,
                                       f"Point: ",
                                       font_size=1.5)
            text_point.color = glm.vec4(0.1, 0.1, 0.1, 1)
            text_point.pivot = Pivot.Center
            text_point.position.relative.center = glm.vec2(0.2, 0.7)
            text_point.update_position()

            input_field_point = elements.InputField(f"input_field_point", window.inner_data_block,
                                                    self.win_size,
                                                    self.gui,
                                                    text_size=1.5)
            input_field_point.position.relative.size = glm.vec2(0.5, 0.15)
            input_field_point.position.relative.center = glm.vec2(0.7, 0.7)
            input_field_point.update_position()
            input_field_point.text.position.relative.left_bottom = glm.vec2(0.05,
                                                                            0.5 - input_field_point.text.position.relative.size.y / 2)
            input_field_point.text.text = ""
            input_field_point.editable = False

            text_plane = elements.Text(f"Plane: ", window.inner_data_block, self.win_size,
                                       f"Plane: ",
                                       font_size=1.5)
            text_plane.color = glm.vec4(0.1, 0.1, 0.1, 1)
            text_plane.pivot = Pivot.Center
            text_plane.position.relative.center = glm.vec2(0.2, 0.5)
            text_plane.update_position()

            input_field_plane = elements.InputField(f"input_field_plane", window.inner_data_block,
                                                    self.win_size,
                                                    self.gui,
                                                    text_size=1.5)
            input_field_plane.position.relative.size = glm.vec2(0.5, 0.15)
            input_field_plane.position.relative.center = glm.vec2(0.7, 0.5)
            input_field_plane.update_position()
            input_field_plane.text.position.relative.left_bottom = glm.vec2(0.05,
                                                                            0.5 - input_field_plane.text.position.relative.size.y / 2)
            input_field_plane.text.text = ""
            input_field_plane.editable = False

            point_component = None
            plane_component = None

            def apply(button, gui, pos):
                nonlocal point_component
                nonlocal plane_component

                if point_component is None or plane_component is None:
                    return
                p1 = point_component.rely_object.transformation.pos
                p2 = plane_component.p1.transformation.pos
                p3 = plane_component.p2.transformation.pos

                len_n = glm.dot(p1 - p2, plane_component.n)
                p2 = p2 + plane_component.n * len_n
                p3 = p3 + plane_component.n * len_n

                point2 = object_creator_m.ObjectCreator.create_point(glm.vec4(1))
                point2.transformation.pos = p2
                self.editor_gui.app.level.objects[point2.id] = point2

                point3 = object_creator_m.ObjectCreator.create_point(glm.vec4(1))
                point3.transformation.pos = p3
                self.editor_gui.app.level.objects[point3.id] = point3

                plane = object_creator_m.ObjectCreator.create_plane_by_3_points(point_component.rely_object, point2,
                                                                                point3)
                self.editor_gui.app.level.objects[plane.id] = plane
                self.update_content()
                window.close()

            button_apply = elements.Button("Apply", window.inner_data_block, self.win_size, self.gui, 'Create', 1.5,
                                           apply,
                                           color=glm.vec4(0, 0.8, 0, 1), text_color=glm.vec4(1))
            button_apply.position.relative.center = glm.vec2(0.65, 0.05)
            button_apply.position.relative.size = glm.vec2(0.3, 0.15)
            button_apply.update_position()

            def clear_fields(button, gui, pos):
                nonlocal point_component
                nonlocal plane_component
                point_component = None
                input_field_point.text.text = ""
                plane_component = None
                input_field_point.text.text = ""

            button_clear = elements.Button("Clear", window.inner_data_block, self.win_size, self.gui, 'Clear', 1.5,
                                           clear_fields,
                                           color=glm.vec4(0.8, 0.8, 0, 1), text_color=glm.vec4(1))
            button_clear.position.relative.center = glm.vec2(0.05, 0.05)
            button_clear.position.relative.size = glm.vec2(0.3, 0.15)
            button_clear.update_position()

            window.update_position()

            def handle_select_element(obj_id):
                nonlocal plane_component
                nonlocal point_component
                obj = self.editor_gui.app.level.objects[obj_id]
                point = obj.get_component_by_name("Point")
                if point:
                    input_field_point.text.text = obj.name
                    point_component = point
                    return
                plane = obj.get_component_by_name("Plane")
                if plane:
                    input_field_plane.text.text = obj.name
                    plane_component = plane
                    return

            def handle_unselect_element(obj_id):
                nonlocal plane_component
                nonlocal point_component
                if obj_id == point_component.rely_object.id:
                    point_component = None
                    input_field_point.text.text = ""
                    return
                if obj_id == plane_component.rely_object.id:
                    plane_component = None
                    input_field_plane.text.text = ""
                    return

            self.select_element += handle_select_element
            self.unselect_element += handle_unselect_element

            self.gui.windows.append(window)

        self._create_button_in_sub_menu(self.sub_menu_plane, create_ask_window_element_1, "By 3 points", 2, 0.2)
        self._create_button_in_sub_menu(self.sub_menu_plane, create_ask_window_element_2, "By point and segment", 3,
                                        0.2)
        self._create_button_in_sub_menu(self.sub_menu_plane, create_ask_window_element_3, "By point and plane", 4)

    def _init_sub_menu_polyhedrons(self):
        self.sub_menu_polyhedrons = elements.Content("Sub Menu polyhedrons", self, self.win_size,
                                                     (1, 1, 1, 0.5))
        self.sub_menu_polyhedrons.position.relative.center = glm.vec2(0.5)
        self.sub_menu_polyhedrons.position.evaluate_values_by_relative()
        self.sub_menu_polyhedrons.active = False

        def create_tetrahedron(button, gui, pos):
            self.editor_gui.app.level.add_object(object_creator_m.ObjectCreator.create_tetrahedron('gray_lit'))

        def create_octahedron(button, gui, pos):
            self.editor_gui.app.level.add_object(object_creator_m.ObjectCreator.create_octahedron('gray_lit'))

        def create_cube(button, gui, pos):
            self.editor_gui.app.level.add_object(object_creator_m.ObjectCreator.create_cube('gray_lit'))

        self._create_button_in_sub_menu(self.sub_menu_polyhedrons, create_tetrahedron, "Tetrahedron", 1, 0.2)
        self._create_button_in_sub_menu(self.sub_menu_polyhedrons, create_octahedron, "Octahedron", 2,
                                        0.2)
        self._create_button_in_sub_menu(self.sub_menu_polyhedrons, create_cube, "Cube", 3)

    def _init_sub_menu_other(self):
        self.sub_menu_other = elements.Content("Sub Menu other", self, self.win_size,
                                               (1, 1, 1, 0.5))
        self.sub_menu_other.position.relative.center = glm.vec2(0.5)
        self.sub_menu_other.position.evaluate_values_by_relative()
        self.sub_menu_other.active = False

        def create_light(button, gui, pos):
            self.editor_gui.app.level.light = self.editor_gui.app.level.add_object(
                object_creator_m.ObjectCreator.create_light()).get_component_by_name("Light")

        self._create_button_in_sub_menu(self.sub_menu_other, create_light, "Create Light", 1, 0.2)

    def _create_button_in_sub_menu(self, sub_menu, action, text, number, content_width=0.13):
        content_element = elements.Block(f"Element_{number}_in_sub_menu_{sub_menu.name}", None, self.win_size,
                                         (1, 1, 1, 0.5))
        content_element.position.relative_window.size = glm.vec2(content_width, 0.05)
        content_element.position.evaluate_values_by_relative_window()

        button = elements.Button(f"{text}_Button", content_element, self.win_size, self.gui,
                                 text,
                                 action=action,
                                 color=glm.vec4(0.5, 0.5, 0.5, 1),
                                 text_size=1
                                 )

        button.position.relative.size = glm.vec2(0.9, 0.8)
        button.position.relative.center = glm.vec2(0.5)
        button.position.evaluate_values_by_relative()
        button.update_position()

        sub_menu.add(content_element)

    def update_content(self):
        self.content.clear()
        self.selected_elements.clear()

        def click_button_action(button, gui, pos):
            name = button.rely_element.name
            obj_id = int(re.search(r'\d+', name).group())
            if input_manager_m.InputManager.keys[pg.K_LCTRL]:
                self.unselect_element(obj_id)
                button.color = glm.vec4(0.7, 0.7, 0.7, 1)
                for element in self.selected_elements:
                    if element[1] == obj_id:
                        self.selected_elements.remove((button, obj_id))
                        return
                return

            if not input_manager_m.InputManager.keys[pg.K_LSHIFT]:
                self.unselect_all_elements_in_content()

            self.select_element(obj_id)

            button.color = glm.vec4(0.6, 0.6, 0.6, 1)

            self.selected_elements.append((button, obj_id))
            object_picker_m.ObjectPicker.select_object(obj_id)

        for obj in self.editor_gui.app.level.objects.values():
            self._create_element_in_content(self.content, click_button_action, obj.name, obj.id)

    def select_element_in_hierarchy(self, object_id):
        for element in self.content.elements[0].elements:
            obj_id = int(re.search(r'\d+', element.name).group())
            if obj_id == object_id:
                element.elements[0].handle_left_click(glm.vec2())
                return

    def unselect_all_elements_in_content(self):
        for selected_elements in self.selected_elements:
            selected_elements[0].color = glm.vec4(0.7, 0.7, 0.7, 1)
        self.selected_elements.clear()

    def delete(self):
        input_manager_m.InputManager.handle_keyboard_press -= self._handle_delete_objs

        self.gui = None
        self.main_block = None
        self.selected_elements.clear()
        del self.select_element
        del self.unselect_element
        self.sub_menu = None
        self.sub_menu_plane = None
        self.sub_menu_other = None
        self.content = None
        super().delete()
