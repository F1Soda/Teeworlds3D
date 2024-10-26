import glm
import moderngl as mgl
import Scripts.Source.General.Managers.index_manager as index_manager_m
import Scripts.Source.General.Managers.input_manager as input_manager_m
import Scripts.Source.General.utils as utils_m


class ObjectPicker:
    _pick_fbo = None  # type: mgl.Framebuffer
    _editor = None

    active_axis = None
    _last_picked_obj_id = 0
    last_picked_obj_transformation = None
    _last_picked_obj_m_model = None
    _last_picked_obj_material = None
    _last_mouse_dot = 0

    @staticmethod
    def init(editor):
        ObjectPicker._editor = editor
        ObjectPicker._pick_fbo = editor.ctx.framebuffer(
            color_attachments=[editor.ctx.texture((int(editor.win_size.x), int(editor.win_size.y)), 4, dtype='f4')],
            depth_attachment=editor.ctx.depth_renderbuffer((int(editor.win_size.x), int(editor.win_size.y)))
        )

        input_manager_m.InputManager.handle_left_click_event += ObjectPicker.process_left_click
        input_manager_m.InputManager.handle_left_hold_event += ObjectPicker.process_hold_left_mouse_button
        input_manager_m.InputManager.handle_left_release_event += ObjectPicker.process_release_left_mouse_button

    @staticmethod
    def process_window_resize(new_size):
        if ObjectPicker._pick_fbo:
            ObjectPicker._pick_fbo.depth_attachment.release()
            ObjectPicker._pick_fbo.color_attachments[0].release()
            ObjectPicker._pick_fbo.release()
        ObjectPicker._pick_fbo = ObjectPicker._editor.ctx.framebuffer(
            color_attachments=[ObjectPicker._editor.ctx.renderbuffer((int(new_size.x), int(new_size.y)))],
            depth_attachment=ObjectPicker._editor.ctx.depth_renderbuffer((int(new_size.x), int(new_size.y)))
        )

    @staticmethod
    def get_object_id_at_pos(pos: glm.vec2):
        pixel = ObjectPicker._pick_fbo.read(attachment=0, viewport=(int(pos.x), int(pos.y), 1, 1))

        return index_manager_m.IndexManager.get_id_by_color(pixel)

    @staticmethod
    def process_left_click(mouse_position):
        object_id = ObjectPicker.get_object_id_at_pos(mouse_position)
        if object_id != 0:
            gizmos_axis = ObjectPicker._editor.level.transform_axis_gizmo.get(object_id)
            if gizmos_axis:
                ObjectPicker.process_click_transformation_gizmos(gizmos_axis, mouse_position)
            else:
                ObjectPicker._editor.editor_gui.select_element_in_hierarchy(object_id)
                ObjectPicker.process_click_object(object_id)
            return True
        else:
            ObjectPicker._editor.editor_gui.unselect_data_in_hierarchy()
            ObjectPicker.process_click_nowhere()
            return False

    @staticmethod
    def process_click_transformation_gizmos(axis, mouse_pos):
        if ObjectPicker.active_axis and ObjectPicker.active_axis != axis:
            ObjectPicker.active_axis.set_default_size()
        ObjectPicker._last_picked_obj_m_model = ObjectPicker.last_picked_obj_transformation.m_model
        ObjectPicker._last_mouse_dot = ObjectPicker.get_dot_with_axis_and_mouse_pos(axis, mouse_pos,
                                                                                    ObjectPicker._last_picked_obj_m_model)
        ObjectPicker.active_axis = axis
        ObjectPicker.active_axis.size = 10.0

    @staticmethod
    def process_click_object(object_id):
        if ObjectPicker.active_axis:
            ObjectPicker.active_axis.set_default_size()
            ObjectPicker.active_axis = None
        ObjectPicker.select_object(object_id)

    @staticmethod
    def select_object(object_id):
        if object_id != ObjectPicker._last_picked_obj_id:
            ObjectPicker._last_picked_obj_id = object_id
            ObjectPicker.last_picked_obj_transformation = ObjectPicker._editor.level.objects[object_id].transformation

    @staticmethod
    def unselect_object():
        ObjectPicker._last_picked_obj_material = None
        ObjectPicker.last_picked_obj_transformation = None
        ObjectPicker._last_picked_obj_id = 0

    @staticmethod
    def process_click_nowhere():
        if ObjectPicker.active_axis:
            ObjectPicker.active_axis.set_default_size()
            ObjectPicker.active_axis = None
        if ObjectPicker._last_picked_obj_id != 0:
            ObjectPicker.unselect_object()

    @staticmethod
    def process_release_left_mouse_button(mouse_pos):
        axis = ObjectPicker.active_axis
        if axis:
            axis.set_default_size()
            ObjectPicker.active_axis = None
            return True
        return False

    @staticmethod
    def picking_pass():
        ObjectPicker._pick_fbo.use()
        ObjectPicker._editor.ctx.clear(0.0, 0.0, 0.0)
        picking_color = glm.vec4(1)
        for obj in ObjectPicker._editor.level.objects.values():
            renderer = obj.get_component_by_name('Renderer')
            if renderer:
                utils_m.copy_vec(index_manager_m.IndexManager.get_color_by_id(obj.id), picking_color)
                renderer.picking_material['color'] = picking_color
                renderer.render_picking_material()
                continue
            point_component = obj.get_component_by_name('Point')
            if point_component:
                last_color = point_component.gizmos_point.color
                utils_m.copy_vec(index_manager_m.IndexManager.get_color_by_id(obj.id), picking_color)
                point_component.gizmos_point.color = picking_color
                point_component.apply()
                point_component.gizmos_point.color = last_color
                continue

        if ObjectPicker._last_picked_obj_id != 0:
            for axis in ObjectPicker._editor.level.transform_axis_gizmo.values():
                # Возможно тут потом какие то преколюхи возникнут, хз зачем выключаю
                ObjectPicker._editor.ctx.disable(mgl.DEPTH_TEST)
                past_color = axis.color
                past_size = axis.size
                axis.size = 20
                axis.color = glm.vec3(index_manager_m.IndexManager.get_color_by_id(axis.id))
                axis.vao.render(mgl.LINES)
                axis.color = past_color
                axis.size = past_size
                ObjectPicker._editor.ctx.enable(mgl.DEPTH_TEST)

        ObjectPicker._editor.ctx.screen.use()

    @staticmethod
    def get_dot_with_axis_and_mouse_pos(axis, mouse_pos, m_model):
        p0 = glm.vec4(axis.start, 1.0)
        p1 = glm.vec4(axis.end, 1.0)
        m_mvp = axis.camera.m_proj * axis.camera.m_view * m_model

        # clip space
        p0 = (m_mvp * p0)
        p1 = (m_mvp * p1)

        # ndc
        ndc_p0 = p0 / p0.w
        ndc_p1 = p1 / p1.w

        # Screen coordinates:
        screen_p0 = glm.vec2((ndc_p0.x + 1.0) * ObjectPicker._editor.win_size[0],
                             (ndc_p0.y) * ObjectPicker._editor.win_size[1]) * 0.5
        screen_p1 = glm.vec2((ndc_p1.x + 1.0) * ObjectPicker._editor.win_size[0],
                             (ndc_p1.y) * ObjectPicker._editor.win_size[1]) * 0.5

        dot = glm.dot(mouse_pos - screen_p0, glm.normalize(screen_p1 - screen_p0))
        return dot

    @staticmethod
    def process_hold_left_mouse_button(current_pos):
        axis = ObjectPicker.active_axis
        if axis is None:
            return False

        dot = ObjectPicker.get_dot_with_axis_and_mouse_pos(axis, current_pos,
                                                           ObjectPicker._last_picked_obj_m_model)
        difference = dot - ObjectPicker._last_mouse_dot
        ObjectPicker._last_mouse_dot = dot
        ObjectPicker.last_picked_obj_transformation.pos = ObjectPicker.last_picked_obj_transformation.pos + (axis.end - axis.start) * difference / 100
        return True

    @staticmethod
    def release():
        ObjectPicker._pick_fbo.depth_attachment.release()
        ObjectPicker._pick_fbo.color_attachments[0].release()
        ObjectPicker._pick_fbo.release()
        ObjectPicker._pick_fbo = None
        ObjectPicker._editor = None
        input_manager_m.InputManager.handle_left_click_event -= ObjectPicker.process_left_click
        input_manager_m.InputManager.handle_left_hold_event -= ObjectPicker.process_hold_left_mouse_button
        input_manager_m.InputManager.handle_left_release_event -= ObjectPicker.process_release_left_mouse_button
