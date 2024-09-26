import numpy as np

import Scripts.Source.Render.library as library
import moderngl as mgl
import glm
import Scripts.GUI.Editor.editor_gui as gui_m
import Scripts.Source.General.Game.object as object_m
import Scripts.Source.Components.components as components
import Scripts.Source.Render.library as library_m
import Scripts.Source.General.Managers.object_picker as object_picker_m
import Scripts.Source.General.Managers.object_creator as object_creator_m
import Scripts.Source.Components.light as light_m


class Gizmos:
    class SegmentByPoints:
        def __init__(self, ctx, p1: object_m.Object, p2: object_m.Object, color: glm.vec4, camera_component, size=3.0,
                     save_size=True):
            # self.id = index_manager_m.IndexManager.get_id()
            self.ctx = ctx
            self.p1 = p1
            self.p2 = p2
            self._color = color
            self._size = self.default_size = size
            self.camera_component = camera_component
            self.save_size = save_size
            self.shader_program = library_m.shader_programs['segment_gizmo']

            self.vbo = None
            self.vao = None

        def init(self, ctx):
            self.ctx = ctx
            self.vbo = self.ctx.buffer(self.get_vertices())
            self.vao = self.ctx.vertex_array(self.shader_program.bin_program, self.vbo, 'in_position')

        def get_vertices(self):
            if self.p1 is None or self.p2 is None:
                return None
            return np.array([self.p1.transformation.pos, self.p2.transformation.pos], dtype=np.float32)

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            if isinstance(value, tuple):
                self._color = glm.vec4(value)
            else:
                self._color = value
            self.shader_program['color'].write(self._color)

        @property
        def size(self):
            return self._size

        @size.setter
        def size(self, value):
            self._size = value
            self.ctx.line_width = value

        def set_default_size(self):
            self.size = self.default_size

        def draw(self, m_model=None, m_proj=None):
            vertices = self.get_vertices()
            if vertices is None:
                return
            self.vbo.write(vertices)

            self.shader_program['color'] = self.color
            self.shader_program['m_proj'].write(m_proj if m_proj is not None else self.camera_component.m_proj)
            self.shader_program['m_view'].write(self.camera_component.m_view)
            self.shader_program['m_model'].write(m_model if m_model is not None else glm.mat4())

            if not self.save_size:
                distance = glm.distance(self.camera_component.transformation.pos,
                                        (self.p1.transformation.pos + self.p2.transformation.pos) / 2)
                scale = 1 / distance
                self.ctx.line_width = self.size * scale
            self.vao.render(mgl.LINES)

        def delete(self):
            self.ctx = None
            self.vbo.release()
            self.vbo = None
            self.vao.release()
            self.vao = None
            self.p1 = None
            self.p2 = None
            self.shader_program = None

    class WordAxisGizmo:
        def __init__(self, ctx, start, end, color, camera, size=3.0, save_size=False, axis_id=None):
            if axis_id:
                self.id = axis_id
            else:
                self.id = camera.app.level.index_manager.get_id()
            self.ctx = ctx
            self.save_size = save_size
            self.start = glm.vec3(*start)
            self._size = self.default_size = size
            self.end = glm.vec3(*end)
            self._color = glm.vec3(color)
            self.shader = library.shader_programs['word_axis_gizmo']
            self.shader['color'].write(self._color)
            self.vao = library.get_segment_vao(ctx, start, end)
            self.camera = camera

        @property
        def size(self):
            return self._size

        @size.setter
        def size(self, value):
            self._size = value
            self.ctx.line_width = value

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            if isinstance(value, tuple):
                self._color = glm.vec3(value)
            else:
                self._color = value
            self.shader['color'].write(self._color)

        def set_default_size(self):
            self.size = self.default_size

        def draw(self, m_model=None, m_proj=None, m_view=None):
            if self.shader.get('m_view'):
                self.shader.get('m_view').write(self.camera.m_view if m_view is None else m_view)
            if self.shader.get('m_model'):
                self.shader.get('m_model').write(m_model)
            if self.shader.get('m_proj'):
                self.shader.get('m_proj').write(self.camera.m_proj if m_proj is None else m_proj)
            self.ctx.line_width = self.size
            self.shader['color'].write(self._color)
            self.vao.render(mgl.LINES)

        def delete(self):
            self.ctx = None
            self.vao.release()
            self.vao = None
            self.shader = None

    class Point:
        def __init__(self, ctx, pos: glm.vec3, color, camera_component, size=10.0, save_size=True):
            # self.id = index_manager_m.IndexManager.get_id()
            self.ctx = ctx
            self._pos = pos
            self.save_size = save_size
            self._size = self.default_size = size
            self._color = glm.vec4(color)
            self.shader = library.shader_programs['point_gizmo']
            self.shader['color'].write(self._color)
            self.vao = library.vaos['point']
            self.camera = camera_component

        @property
        def pos(self):
            return self._pos

        @pos.setter
        def pos(self, value):
            if isinstance(value, tuple):
                self._pos = glm.vec3(value)
            else:
                self._pos = value
            self.shader['position'].write(self._pos)

        @property
        def size(self):
            return self._size

        @size.setter
        def size(self, value):
            self._size = value
            self.ctx.line_width = value

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            if isinstance(value, tuple):
                self._color = glm.vec4(value)
            else:
                self._color = value
            self.shader['color'].write(self._color)

        def set_default_size(self):
            self.size = self.default_size

        def draw(self, m_proj=None, m_view=None):

            if self.shader.get('m_view'):
                self.shader.get('m_view').write(self.camera.m_view if m_view is None else m_view)
            if self.shader.get('m_proj'):
                self.shader.get('m_proj').write(self.camera.m_proj if m_proj is None else m_proj)
            if self.save_size:
                self.ctx.point_size = self.size
            else:
                distance = glm.distance(self.camera.transformation.pos, self.pos)
                scale = 1 / distance
                self.ctx.point_size = self.size * scale
            self.shader['color'].write(self._color)
            self.shader['position'].write(self._pos)
            self.vao.render(mgl.POINTS)

        def delete(self):
            self.ctx = None
            self.camera = None
            self.shader = None
            self.vao = None

    def __init__(self, ctx: mgl.Context, scene):
        self.ctx = ctx
        self.camera = scene.camera_component
        self.scene = scene
        self.x_axis_in_right_corner = Gizmos.WordAxisGizmo(ctx, (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
                                                           glm.vec3(1, 0, 0),
                                                           self.scene.camera_component, axis_id=-1)
        self.y_axis_in_right_corner = Gizmos.WordAxisGizmo(ctx, (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5),
                                                           glm.vec3(0, 1, 0),
                                                           self.scene.camera_component, axis_id=-1)
        self.z_axis_in_right_corner = Gizmos.WordAxisGizmo(ctx, (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5),
                                                           glm.vec3(0, 0, 1),
                                                           self.scene.camera_component, axis_id=-1)

        self.x_axis_center = Gizmos.WordAxisGizmo(ctx, (-3, 0.1, 0), (3, 0.1, 0), glm.vec3(0.8, 0, 0),
                                                  self.scene.camera_component, axis_id=-1)
        self.y_axis_center = Gizmos.WordAxisGizmo(ctx, (0, -3, 0), (0, 3, 0), glm.vec3(0, 0.8, 0),
                                                  self.scene.camera_component, axis_id=-1)
        self.z_axis_center = Gizmos.WordAxisGizmo(ctx, (0, 0.1, -3), (0, 0.1, 3), glm.vec3(0, 0, 0.8),
                                                  self.scene.camera_component, axis_id=-1)

        # Gizmos Light
        gizmos_light = object_m.Object(scene, 'gizmos_light', obj_id=-1)
        gizmos_light.transformation.pos = glm.vec3(3, 6, 3)
        self.gizmos_light_component = gizmos_light.add_component(light_m.Light())

        # Arrows for center coordinate axis
        current_index = scene.index_manager.global_index

        self.arrow_axis_renderers = []
        arrow_x_axis = object_creator_m.ObjectCreator.create_tetrahedron("red_lit", add_to_sequence_render=False)
        arrow_x_axis.transformation.pos = glm.vec3(3, 0.1, 0)
        arrow_x_axis.transformation.rot = glm.vec3(0, 0, -90)
        arrow_x_axis.transformation.scale = glm.vec3(0.2)
        arrow_x_axis.id = -1
        self.arrow_axis_renderers.append(arrow_x_axis.get_component_by_name("Renderer"))
        self.arrow_axis_renderers[0].material.light_component = self.gizmos_light_component

        arrow_y_axis = object_creator_m.ObjectCreator.create_tetrahedron("green_lit", add_to_sequence_render=False)
        arrow_y_axis.transformation.pos = glm.vec3(0, 3, 0)
        arrow_y_axis.transformation.rot = glm.vec3(0, 0, 0)
        arrow_y_axis.transformation.scale = glm.vec3(0.2)
        arrow_y_axis.id = -1
        self.arrow_axis_renderers.append(arrow_y_axis.get_component_by_name("Renderer"))
        self.arrow_axis_renderers[1].material.light_component = self.gizmos_light_component

        arrow_z_axis = object_creator_m.ObjectCreator.create_tetrahedron("blue_lit", add_to_sequence_render=False)
        arrow_z_axis.transformation.pos = glm.vec3(0, 0.1, 3)
        arrow_z_axis.transformation.rot = glm.vec3(90, 0, 0)
        arrow_z_axis.transformation.scale = glm.vec3(0.2)
        arrow_z_axis.id = -1
        self.arrow_axis_renderers.append(arrow_z_axis.get_component_by_name("Renderer"))
        self.arrow_axis_renderers[2].material.light_component = self.gizmos_light_component

        scene.index_manager.global_index = current_index

        plane = object_m.Object(scene, "Plane", [], obj_id=-1)
        renderer = components.Renderer(library_m.meshes['plane'], library_m.materials['grid'])
        plane.add_component(renderer)
        plane.transformation.scale = glm.vec3(1000, 1, 1000)
        renderer.material['tilling'] = glm.vec2(1000)
        renderer.material['color'] = glm.vec4(1, 1, 1, 0.5)

        self.grid_plane_renderer = renderer
        self.shader = library.shader_programs['word_axis_gizmo']
        self.draw_grid_and_center_system = True

    def process_window_resize(self, new_win_size):
        self.grid_plane_renderer.update_projection_matrix(self.camera.m_proj)
        for arrow_axis_renderer in self.arrow_axis_renderers:
            arrow_axis_renderer.update_projection_matrix(self.camera.m_proj)

    def draw_center_axis_arrows(self):
        for renderer in self.arrow_axis_renderers:
            renderer.material.update(renderer.rely_object.transformation, self.gizmos_light_component)
            renderer.vao.render()

    def render(self):
        self.ctx.enable(mgl.BLEND)
        self.draw_word_axis_in_right_corner()
        transform = object_picker_m.ObjectPicker.last_picked_obj_transformation
        if self.draw_grid_and_center_system:
            self.draw_center_coordinate()
            self.draw_center_axis_arrows()
            self.draw_plane_grid()
        if transform and transform.moveable:
            self.ctx.disable(mgl.DEPTH_TEST)
            self.scene.draw_gizmos_transformation_axis(object_picker_m.ObjectPicker.last_picked_obj_transformation)
            self.ctx.enable(mgl.DEPTH_TEST)
        self.ctx.disable(mgl.BLEND)

    def draw_center_coordinate(self):
        self.x_axis_center.draw(glm.mat4())
        self.y_axis_center.draw(glm.mat4())
        self.z_axis_center.draw(glm.mat4())

    def draw_word_axis_in_right_corner(self):
        self.x_axis_in_right_corner.draw(m_proj=self.camera.m_ortho, m_model=self.get_model_matrix_for_world_axis())
        self.y_axis_in_right_corner.draw(m_proj=self.camera.m_ortho, m_model=self.get_model_matrix_for_world_axis())
        self.z_axis_in_right_corner.draw(m_proj=self.camera.m_ortho, m_model=self.get_model_matrix_for_world_axis())

    def draw_plane_grid(self):
        self.grid_plane_renderer.apply()

    def get_model_matrix_for_world_axis(self):
        m_model = glm.mat4()
        near = self.camera.near
        diagonal = pow(self.ctx.screen.width * self.ctx.screen.width +
                       self.ctx.screen.height * self.ctx.screen.height, 0.5)
        size = near / diagonal * 150
        up = self.camera.up
        right = self.camera.right
        forward = self.camera.forward
        m_model = glm.translate(m_model, self.camera.transformation.pos
                                + forward * (self.camera.near + 1)
                                + right * (self.camera.right_bound * (gui_m.EditorGUI.LEFT_INSPECTOR_CORNER - 0.5) * 2)
                                - up * (self.camera.top_bound)
                                + (up - right) * size
                                )

        m_model = glm.scale(m_model, (size, size, size))
        return m_model

    def delete(self):
        self.ctx = None
        self.camera = None
        self.scene = None
        self.x_axis_in_right_corner.delete()
        self.x_axis_in_right_corner = None
        self.y_axis_in_right_corner.delete()
        self.y_axis_in_right_corner = None
        self.z_axis_in_right_corner.delete()
        self.z_axis_in_right_corner = None

        self.x_axis_center.delete()
        self.x_axis_center = None
        self.y_axis_center.delete()
        self.y_axis_center = None
        self.z_axis_center.delete()
        self.z_axis_center = None

        self.gizmos_light_component.rely_object.delete()
        self.gizmos_light_component = None
        for arrow_axis_renderer in self.arrow_axis_renderers:
            arrow_axis_renderer.rely_object.delete()
        self.arrow_axis_renderers.clear()

        self.grid_plane_renderer.rely_object.delete()
        self.grid_plane_renderer = None
        self.shader = None
