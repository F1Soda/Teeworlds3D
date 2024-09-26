import Scripts.Source.Components.components as components_m
import Scripts.Source.General.Game.object as object_m
import Scripts.Source.Render.library as library_m
import Scripts.Source.Render.render as render
import Scripts.Source.General.utils as utils_m
import json
import glm
import re


class DataManager:
    letters_width = []
    empty_scene_data = {
        "index_manager_data": {
            "global_index": 5,
            "unused_indices": []
        },
        "objects": {}
    }

    @staticmethod
    def parse_letter_widths(file_path):
        letter_widths = []

        with open(file_path, 'r') as f:
            for line in f:
                # Each line is expected to be in the format "Letter {idx}: {width}"
                parts = line.strip().split(': ')
                if len(parts) == 2:
                    width = float(parts[1])
                    letter_widths.append(width)

        return letter_widths

    @staticmethod
    def init():
        DataManager.letters_width = DataManager.parse_letter_widths('Data/letter_width.txt')

    @staticmethod
    def update_letters_width():
        DataManager.letter_widths = utils_m.calculate_width_letters('textures/Verdana_B_alpha.png')
        with open('Data/letter_width.txt', 'w') as f:
            for idx, width in enumerate(DataManager.letter_widths):
                f.write(f"Letter {idx}: {width}\n")

    @staticmethod
    def save_scene(scene, file_path):
        with open(file_path, 'w') as f:
            save = {'index_manager_data': scene.index_manager.serialize(), 'objects': {}}
            for obj in scene.objects.values():
                temp_data = obj.serialize()
                save['objects'][obj.id] = temp_data

            json.dump(save, f, indent=4)

    @staticmethod
    def load_scene(scene, file_path):
        later_initialization_dict = {}
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                scene.index_manager.global_index = data['index_manager_data']['global_index']
                scene.index_manager.unused_indices = data['index_manager_data']['unused_indices']
                for obj_id, obj_data in data['objects'].items():
                    obj_id = int(obj_id)
                    obj = object_m.Object(scene, "None", obj_id=obj_id)
                    for key, value in obj_data.items():
                        if key == "name":
                            obj.name = value
                        if key == "components":
                            DataManager.parse_components(value, obj, later_initialization_dict, scene)
                    scene.objects[obj_id] = obj
            return True
        except json.decoder.JSONDecodeError as e:
            print("Failed to load scene:\n", e)
        except FileNotFoundError:
            with open(file_path, 'w') as f:
                json.dump(DataManager.empty_scene_data, f)

    @staticmethod
    def parse_ref_id(key, value, component_data, rely_obj_id, component_name, scene, later_initialization_dict):
        obj = scene.objects.get(value[1])
        if obj:
            additional_param = re.search(value[0], r'(?<=\.).+')
            res_value = obj
            if additional_param:
                res_value = obj.get_component_by_name(additional_param.group())
            component_data[key] = res_value
        else:
            later_initialization_dict[value[1]] = (rely_obj_id, component_name, key, value[0])

    @staticmethod
    def later_initialization(obj, later_initialization_dict, scene):
        data = later_initialization_dict[obj.id]
        scene.objects[data[0]].get_component_by_name(data[1]).__setitem__(data[2], obj.id)
        later_initialization_dict.pop(obj.id)

    @staticmethod
    def parse_glm_vec(key, value, component_data):
        if len(value[1]) == 2:
            value = glm.vec2(value[1])
        elif len(value[1]) == 3:
            value = glm.vec3(value[1])
        elif len(value[1]) == 4:
            value = glm.vec4(value[1])
        component_data[key] = value

    @staticmethod
    def parse_components(components, obj, later_initialization_dict, scene):
        rendering_component = None

        for component_name, component_data in components.items():
            should_create_component = True
            # Parsing non-serializable types and references
            for key, value in component_data.items():
                # glm.vec
                if isinstance(value, list):
                    if value[0] == "vec":
                        DataManager.parse_glm_vec(key, value, component_data)
                    if value[0].startswith('id'):
                        DataManager.parse_ref_id(key, value, component_data, obj.id, component_name, scene,
                                                 later_initialization_dict)

            # Special Cases
            if component_name == "Renderer":
                component_data['mesh'] = library_m.meshes[component_data['mesh']]
                component_data['material'] = library_m.materials[component_data['material']]
            elif component_name == "Transformation":
                obj.transformation.pos = component_data['pos']
                obj.transformation.rot = component_data['rot']
                obj.transformation.scale = component_data['scale']
                obj.transformation.moveable = component_data['moveable']
                should_create_component = False
            elif component_name == "Plane":
                component_data['render_mode'] = render.RenderMode[component_data['render_mode']]

            if should_create_component:
                a = components_m.components[component_name](**component_data)
                component = obj.add_component(a)
                if (isinstance(component, components_m.Point) or
                        isinstance(component, components_m.Segment) or
                        isinstance(component, components_m.Plane) or
                        isinstance(component, components_m.Renderer)):
                    component.update_render_mode()

        if later_initialization_dict.get(obj.id):
            DataManager.later_initialization(obj, later_initialization_dict, scene)
