import glm

import Scripts.Source.General.Managers.object_creator as object_creator_m
import Scripts.Source.Render.gizmos as gizmos_m
import Scripts.Source.General.Managers.data_manager as data_manager_m
import Scripts.Source.General.Managers.index_manager as index_manager_m
import Scripts.Source.Components.components as components
import Scripts.Source.General.Game.object as object_m

DEBUG = False


class Level:
    def __init__(self, app, gui):
        self.app = app
        self.ctx = self.app.ctx
        self.objects = {}
        self.transform_axis_gizmo = {}

        self.index_manager = index_manager_m.IndexManager()

        self.light = None
        self.camera = None
        self.camera_component = None
        self.player = None
        self.player_component = None
        self.player_rb = None

        self.opaque_renderer = []
        self.transparency_renderer = []
        self.test_saving_object = None
        self.render_hidden_lines = components.renderer_m.HiddenLineState.Off

        self.gui = gui

        self.client_wrappers = {}

        self.is_game = None

    def change_hidden_line_mode(self):
        if self.render_hidden_lines == components.renderer_m.HiddenLineState.Off:
            self.render_hidden_lines = components.renderer_m.HiddenLineState.Line
        elif self.render_hidden_lines == components.renderer_m.HiddenLineState.Line:
            self.render_hidden_lines = components.renderer_m.HiddenLineState.Dash
        elif self.render_hidden_lines == components.renderer_m.HiddenLineState.Dash:
            self.render_hidden_lines = components.renderer_m.HiddenLineState.Both
        elif self.render_hidden_lines == components.renderer_m.HiddenLineState.Both:
            self.render_hidden_lines = components.renderer_m.HiddenLineState.Off

    def _default_load(self):

        tetrahedron = object_creator_m.ObjectCreator.create_tetrahedron('blue_lit')
        tetrahedron.transformation.pos = (5, 1, 8)
        tetrahedron.transformation.scale = glm.vec3(2)
        self.objects[tetrahedron.id] = tetrahedron

        octahedron = object_creator_m.ObjectCreator.create_octahedron('red_lit')
        octahedron.transformation.pos = (5, 1, 5)
        octahedron.transformation.scale = glm.vec3(2)
        self.objects[octahedron.id] = octahedron

        cube = object_creator_m.ObjectCreator.create_cube('green_lit')
        cube.transformation.pos = (5, 1, 2)
        cube.transformation.scale = glm.vec3(2)
        self.objects[cube.id] = cube

        p1 = object_creator_m.ObjectCreator.create_point(glm.vec4(1, 0, 0, 1), size=200)
        p1.transformation.pos = glm.vec3(4, 0, 4)
        self.objects[p1.id] = p1

        p2 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 1, 0, 1), size=200)
        p2.transformation.pos = glm.vec3(0, 0, 4)
        self.objects[p2.id] = p2

        test_segment = object_creator_m.ObjectCreator.create_segment(glm.vec4(0.6, 0.1, 0.5, 1), p1, p2)
        self.objects[test_segment.id] = test_segment

        p3 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 0, 1, 1), size=200)
        p3.transformation.pos = glm.vec3(3, 4, 12)
        self.objects[p3.id] = p3

        p4 = object_creator_m.ObjectCreator.create_point(glm.vec4(1, 0, 1, 1), size=200)
        p4.transformation.pos = glm.vec3(3, 6, 14)
        self.objects[p4.id] = p4

        p5 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 1, 1, 1), size=200)
        p5.transformation.pos = glm.vec3(5, 2, 12)
        self.objects[p5.id] = p5

        plane_by_3_points = object_creator_m.ObjectCreator.create_plane_by_3_points(p3, p4, p5)
        self.objects[plane_by_3_points.id] = plane_by_3_points

        p6 = object_creator_m.ObjectCreator.create_point(glm.vec4(0.2, 0.5, 0.4, 1), size=200)
        p6.transformation.pos = glm.vec3(1, 1, 1)
        self.objects[p6.id] = p6

        center_segment_cube = glm.vec3(5, 1, -2)
        for x in [-1, 1]:
            for y in [-1, 1]:
                for z in [-1, 1]:
                    point_in_segment_cube = object_creator_m.ObjectCreator.create_point(glm.vec4(1, 1, 1, 1), size=200)
                    point_in_segment_cube.transformation.pos = glm.vec3(x, y, z) + center_segment_cube
                    self.objects[point_in_segment_cube.id] = point_in_segment_cube

        ########################################################################################################

        cube = object_creator_m.ObjectCreator.create_cube('transparency_white_unlit')
        cube_renderer = cube.get_component_by_name('Renderer')
        cube.transformation.pos = glm.vec3(5, 1, -6)
        cube.transformation.scale = glm.vec3(2)
        cube.add_component(components.Secateur())
        self.objects[cube.id] = cube

        p1 = object_creator_m.ObjectCreator.create_point(glm.vec4(1, 0, 0, 1), size=200)
        p1.transformation.pos = glm.vec3(6, 0, -7)
        self.objects[p1.id] = p1

        p2 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 1, 0, 1), size=200)
        p2.transformation.pos = glm.vec3(4, 2, -5)
        self.objects[p2.id] = p2

        p3 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 0, 1, 1), size=200)
        p3.transformation.pos = glm.vec3(6, 2, -5)
        self.objects[p3.id] = p3

        plane = object_creator_m.ObjectCreator.create_plane_by_3_points(p1, p2, p3)
        plane.add_component(components.Section(inverse=False))
        self.objects[plane.id] = plane

        #######################################################################################

        cube = object_creator_m.ObjectCreator.create_cube('transparency_white_unlit')
        cube_renderer = cube.get_component_by_name('Renderer')
        cube.transformation.pos = glm.vec3(5, 1, -12)
        cube.transformation.scale = glm.vec3(2)
        cube.add_component(components.Secateur())
        # cube.add_component(components.Translator(speed=1, radius=2))
        self.objects[cube.id] = cube

        p1 = object_creator_m.ObjectCreator.create_point(glm.vec4(1, 0, 0, 1), size=200)
        p1.transformation.pos = glm.vec3(6, 0, -13)
        self.objects[p1.id] = p1

        p2 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 1, 0, 1), size=200)
        p2.transformation.pos = glm.vec3(4, 2, -11)
        self.objects[p2.id] = p2

        p3 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 0, 1, 1), size=200)
        p3.transformation.pos = glm.vec3(6, 2, -11)
        self.objects[p3.id] = p3

        plane = object_creator_m.ObjectCreator.create_plane_by_3_points(p1, p2, p3)
        plane.add_component(components.Section(inverse=True))
        self.objects[plane.id] = plane

        #########################################################################################3333

        cube = object_creator_m.ObjectCreator.create_cube('transparency_white_unlit')
        cube_renderer = cube.get_component_by_name('Renderer')
        cube.transformation.pos = glm.vec3(5, 1, -20)
        cube.transformation.scale = glm.vec3(2)
        cube.add_component(components.Secateur())
        cube.add_component(
            components.Translator(speed=1, radius=2, translate_by=components.translator_m.Translator.UpDown))
        cube.add_component(
            components.Rotator(speed=1,
                               rotate_by=components.rotator_m.Rotator.X |
                                         components.rotator_m.Rotator.Y |
                                         components.rotator_m.Rotator.Z))
        self.objects[cube.id] = cube

        octahedron = object_creator_m.ObjectCreator.create_octahedron('transparency_white_unlit')
        octahedron_renderer = octahedron.get_component_by_name('Renderer')
        octahedron.transformation.pos = glm.vec3(9, 1, -21)
        octahedron.transformation.scale = glm.vec3(2)
        octahedron.add_component(components.Secateur())
        octahedron.add_component(
            components.Translator(speed=1, radius=3, translate_by=components.translator_m.Translator.LeftRight))
        octahedron.add_component(
            components.Rotator(speed=1,
                               rotate_by=components.rotator_m.Rotator.X))
        self.objects[octahedron.id] = octahedron

        tetrahedron = object_creator_m.ObjectCreator.create_tetrahedron('transparency_white_unlit')
        tetrahedron_renderer = tetrahedron.get_component_by_name('Renderer')
        tetrahedron.transformation.pos = glm.vec3(5, 1, -24)
        tetrahedron.transformation.scale = glm.vec3(2)
        tetrahedron.add_component(components.Secateur())
        tetrahedron.add_component(
            components.Translator(speed=1, radius=2, translate_by=components.translator_m.Translator.ForwardBackward))
        tetrahedron.add_component(
            components.Rotator(speed=1,
                               rotate_by=components.rotator_m.Rotator.Y
                               ))
        self.objects[tetrahedron.id] = tetrahedron

        p1 = object_creator_m.ObjectCreator.create_point(glm.vec4(1, 0, 0, 1), size=200)
        p1.transformation.pos = cube.transformation.pos + glm.vec3(2, 0, -2)
        self.objects[p1.id] = p1

        p2 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 1, 0, 1), size=200)
        p2.transformation.pos = cube.transformation.pos + glm.vec3(-2, 0, -2)
        self.objects[p2.id] = p2

        p3 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 0, 1, 1), size=200)
        p3.transformation.pos = cube.transformation.pos + glm.vec3(2, 0, 2)
        self.objects[p3.id] = p3

        plane = object_creator_m.ObjectCreator.create_plane_by_3_points(p1, p2, p3)
        plane.add_component(components.Section(inverse=True))
        self.objects[plane.id] = plane

        #############################################################3

        cube = object_creator_m.ObjectCreator.create_cube('transparency_white_unlit')
        cube_renderer = cube.get_component_by_name('Renderer')
        cube.transformation.pos = glm.vec3(-6, 1, -20)
        cube.transformation.scale = glm.vec3(2)
        cube.add_component(components.Secateur())
        cube.add_component(
            components.Translator(speed=1, radius=2, translate_by=components.translator_m.Translator.UpDown))
        cube.add_component(
            components.Rotator(speed=1,
                               rotate_by=components.rotator_m.Rotator.X |
                                         components.rotator_m.Rotator.Y |
                                         components.rotator_m.Rotator.Z))
        self.objects[cube.id] = cube

        octahedron = object_creator_m.ObjectCreator.create_octahedron('transparency_white_unlit')
        octahedron_renderer = octahedron.get_component_by_name('Renderer')
        octahedron.transformation.pos = glm.vec3(-2, 1, -21)
        octahedron.transformation.scale = glm.vec3(2)
        octahedron.add_component(components.Secateur())
        octahedron.add_component(
            components.Translator(speed=1, radius=3, translate_by=components.translator_m.Translator.LeftRight))
        octahedron.add_component(
            components.Rotator(speed=1,
                               rotate_by=components.rotator_m.Rotator.X))
        self.objects[octahedron.id] = octahedron

        tetrahedron = object_creator_m.ObjectCreator.create_tetrahedron('transparency_white_unlit')
        tetrahedron_renderer = tetrahedron.get_component_by_name('Renderer')
        tetrahedron.transformation.pos = glm.vec3(-6, 1, -24)
        tetrahedron.transformation.scale = glm.vec3(2)
        tetrahedron.add_component(components.Secateur())
        tetrahedron.add_component(
            components.Translator(speed=1, radius=2, translate_by=components.translator_m.Translator.ForwardBackward))
        tetrahedron.add_component(
            components.Rotator(speed=1,
                               rotate_by=components.rotator_m.Rotator.Y
                               ))
        self.objects[tetrahedron.id] = tetrahedron

        p1 = object_creator_m.ObjectCreator.create_point(glm.vec4(1, 0, 0, 1), size=200)
        p1.transformation.pos = cube.transformation.pos + glm.vec3(2, 0, -2)
        self.objects[p1.id] = p1

        p2 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 1, 0, 1), size=200)
        p2.transformation.pos = cube.transformation.pos + glm.vec3(-2, 0, -2)
        self.objects[p2.id] = p2

        p3 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 0, 1, 1), size=200)
        p3.transformation.pos = cube.transformation.pos + glm.vec3(2, 0, 2)
        self.objects[p3.id] = p3

        plane = object_creator_m.ObjectCreator.create_plane_by_3_points(p1, p2, p3)
        plane.add_component(components.Section(inverse=False))
        self.objects[plane.id] = plane

        ####################################################################

        light = object_creator_m.ObjectCreator.create_light()
        self.objects[light.id] = light

    def load(self, file_path=None, is_game=False):
        self.is_game = is_game
        if is_game and not DEBUG:
            self.player = object_creator_m.ObjectCreator.create_player()

            self.player_rb = self.player.add_component(components.RigidBody(1))
            self.player_rb.restitution = 0
            self.player_rb.static_friction = 0
            self.player_rb.dynamic_friction = 1
            self.player.add_component(components.BoxCollider())

            ground_checker = object_m.Object(self, "Ground Checker", self.player)

            self.player.add_children(ground_checker)

            ground_checker.transformation.pos = ground_checker.transformation.pos - glm.vec3(0, 0.5, 0)
            gc_collider = ground_checker.add_component(components.BoxCollider())
            gc_collider.is_trigger = True
            gc_collider.draw_collider = True
            gc_collider.size = glm.vec3(0.5, 0.2, 0.5)
            gc_collider.use_transform_model_matrix = False

            ground_checker.add_component(components.GroundChecker())

            self.add_object(self.player)

            self.camera = object_creator_m.ObjectCreator.create_camera_in_game(self.player)
            self.camera_component = self.camera.get_component_by_name("Camera")

            player_controller_component = self.player.get_component_by_name("Player Controller")

            self.hookshot_root = object_m.Object(self, "hookshot_root", self.player)
            self.player.add_children(self.hookshot_root)
            self.hookshot_model = hookshot_model = object_creator_m.ObjectCreator.create_cube("orange_unlit",
                                                                                              "hookshot_model")
            hookshot_model.remove_component_by_name("Box Collider")
            hookshot_model.transformation.scale = glm.vec3(0.2, 0.2, 1)
            hookshot_model.transformation.pos = glm.vec3(0, 0, 0.5)
            self.hookshot_root.add_children(hookshot_model)

            self.hookshot_model.enable = False

            player_controller_component.hookshot_transformation = self.hookshot_root.transformation
            player_controller_component.hookshot_model_transformation = self.hookshot_model.transformation
            player_controller_component.camera_component = self.camera_component

            self.player.add_children(self.camera)

            self.player.add_component(components.MeshFilter(object_creator_m.library_m.meshes['cube']))
            # cube_renderer = components.Renderer(object_creator_m.library_m.materials["cyan_unlit"], True)
            # self.player.add_component(cube_renderer)

            # self.opaque_renderer.append(cube_renderer)

            self.camera.transformation.pos = self.camera.transformation.pos + glm.vec3(0, 0.5, 0)

            self.weapon = object_creator_m.ObjectCreator.create_dumpy_weapon()
            self.weapon.remove_component_by_name("Box Collider")
            weapon_component = self.weapon.add_component(components.Weapon(1, 1, 1, 1, "Weapon", "WEP"))
            weapon_component.camera_transformation = self.camera.transformation
            self.player.add_children(self.weapon)
            self.weapon.transformation.pos = self.weapon.transformation.pos + self.player.transformation.right * (
                    0.1 + 1 / 2) + self.player.transformation.forward * (0.2)
            self.player.transformation.pos = self.player.transformation.up

            player_controller_component.debug_box = object_creator_m.ObjectCreator.create_cube("red_unlit", "debug_box")
            player_controller_component.debug_box.transformation.scale = glm.vec3(0.1)
            player_controller_component.camera_component = self.camera_component

            self.player_component = self.player.get_component_by_name("Player")

        else:
            self.camera = object_creator_m.ObjectCreator.create_camera_in_editor()
            self.camera_component = self.camera.get_component_by_name("Camera")
        self.init_gizmo()

        if file_path:
            data_manager_m.DataManager.load_scene(self, file_path)
        else:
            self._default_load()
        for obj in self.objects.values():
            light = obj.get_component_by_name("Light")
            if light:
                self.light = light

    def add_object(self, obj):
        self.objects[obj.id] = obj
        if self.app.NAME == "Editor":
            self.app.editor_gui.update_data_in_hierarchy()
        return obj

    def delete_object(self, obj):
        obj.delete()
        del self.objects[obj.id]
        if self.app.NAME == "Editor":
            self.app.editor_gui.update_data_in_hierarchy()

    def init_gizmo(self):
        axis = gizmos_m.Gizmos.WordAxisGizmo(self.ctx, (0, 0, 0), (1, 0, 0), (1, 0, 0), self.camera_component, size=3)
        self.transform_axis_gizmo[axis.id] = axis
        axis = gizmos_m.Gizmos.WordAxisGizmo(self.ctx, (0, 0, 0), (0, 1, 0), (0, 1, 0), self.camera_component, size=3)
        self.transform_axis_gizmo[axis.id] = axis
        axis = gizmos_m.Gizmos.WordAxisGizmo(self.ctx, (0, 0, 0), (0, 0, 1), (0, 0, 1), self.camera_component, size=3)
        self.transform_axis_gizmo[axis.id] = axis

    def draw_gizmos_transformation_axis(self, transformation):
        for axis in self.transform_axis_gizmo.values():
            distance = glm.distance(self.camera.transformation.pos, transformation.pos)
            scale = distance * 1 / 7
            m_model = glm.scale(transformation.m_tr, glm.vec3(scale))
            axis.draw(m_model)

    def process_window_resize(self, new_size):
        self.camera_component.process_window_resize(new_size)
        for obj in self.objects.values():
            obj.process_window_resize(new_size)

    def on_draw_gizmos(self):
        for obj in self.objects.values():
            obj.on_gizmos(self.camera_component)

    def apply_components(self):
        if self.app.NAME == "Game":
            self.app.game_gui.debug_global_text.text = f"({self.hookshot_root.transformation.rot.x:.2f}, {self.hookshot_root.transformation.rot.y:.2f}, {self.hookshot_root.transformation.rot.z:.2f})"
            self.app.game_gui.debug_LOCAL_text.text = f"({self.hookshot_model.transformation.pos.x:.2f}, {self.hookshot_model.transformation.pos.y:.2f}, {self.hookshot_model.transformation.pos.z:.2f})"

            self.app.game_gui.fps_text.text = f"FPS: {self.app.get_fps():.0f}"
        if not self.is_game:
            self.camera.apply_components()
        for obj in self.objects.values():
            obj.apply_components()

    def fixed_apply_components(self):
        if self.app.NAME == "Game":
            self.app.game_gui.fps_text.text = f"FPS: {self.app.get_fps():.0f}"
        for obj in self.objects.values():
            obj.fixed_apply_components()

    def render_opaque_objects(self):
        # print("render opaque")
        for renderer in self.opaque_renderer:
            if renderer.rely_object.enable and renderer.enable:
                renderer.apply()

    def render_transparent_objects(self):
        for renderer in self.transparency_renderer:
            if renderer.rely_object.enable and renderer.enable:
                renderer.apply()

    def delete(self):
        for obj_id, obj in self.objects.items():
            obj.delete()
        self.objects.clear()

        for obj in self.transform_axis_gizmo.values():
            obj.delete()
        self.transform_axis_gizmo.clear()

        self.camera.delete()
        self.camera_component = None
        self.index_manager = None

    # Server-client
    def get_player_data(self):
        return self.player_component.serialize()

    def spawn_player(self, pos):
        self.player.transformation.pos = pos

    def spawn_client(self, pos, client_id):
        wrapper = object_creator_m.ObjectCreator.create_client_wrapper(client_id)
        wrapper.transformation.pos = pos
        self.add_object(wrapper)
        self.client_wrappers[client_id] = wrapper
    ################
