import typing
import Scripts.Source.Components.Default.component as component_m
import Scripts.Source.Components.Default.transformation as transformation_m
import Scripts.Source.Components.Default.renderer as renderer_m

GLOBAL_INDEX = 0


class Object:
    def __init__(self, level, name: str, parent_object=None,
                 obj_id=None):
        self.level = level
        self.name = name
        self.components: typing.List[component_m.Component] = []
        self.parent_object = parent_object
        self.child_objects = []
        if obj_id:
            self.id = obj_id
        else:
            self.id = level.index_manager.get_id()

        # Transformation
        self.transformation = transformation_m.Transformation()

        self.add_component(self.transformation)

        self.components_to_apply_fixed_update = []
        self.components_to_call_on_gizmos = []

        self._renderer: renderer_m.Renderer = None
        self.enable = True

    def add_children(self, children):
        self.child_objects.append(children)
        self.transformation.add_child(children.transformation)

    def add_component(self, component) -> component_m.Component:
        component.rely_object = self
        component.init(self.level.app, self)
        self.components.append(component)
        component.apply()

        if component.use_fixed_update:
            self.components_to_apply_fixed_update.append(component)

        if component.use_on_draw_gizmos:
            self.components_to_call_on_gizmos.append(component)

        return component

    def remove_component(self, component):
        self.components.remove(component)
        component.delete()

    def remove_component_by_name(self, name):
        for component in self.components:
            if component.name == name:
                self.components.remove(component)
                component.delete()
                return
        raise Exception(f"Could not remove not existing component: {name}")

    def process_window_resize(self, new_size):
        for component in self.components:
            component.process_window_resize(new_size)

    def get_component_by_name(self, name: str) -> component_m.Component | None:
        for component in self.components:
            if component.name == name or component.base_name == name:
                return component
        return None

    def get_component_by_type(self, type_component: type) -> component_m.Component | None:
        for component in self.components:
            if isinstance(component, type_component):
                return component
        return None

    def delete(self):
        for component in self.components:
            component.delete()
        self.components_to_call_on_gizmos = None
        self.components_to_apply_fixed_update = None

    def apply_components(self):
        for component in self.components:
            if component.enable and component.name not in ["Renderer", "Plane"]:
                component.apply()
        for child in self.child_objects:
            child.apply_components()

    def fixed_apply_components(self):
        for component in self.components_to_apply_fixed_update:
            if component.enable:
                component.fixed_apply()
        for child in self.child_objects:
            child.fixed_apply_components()

    def on_gizmos(self, camera_component):
        for component in self.components_to_call_on_gizmos:
            if component.enable:
                component.on_gizmos(camera_component)
        for child in self.child_objects:
            child.on_gizmos(camera_component)

    def serialize(self):
        return {
            'name': self.name,
            'components': {
                component.name: component.serialize() for component in self.components
            }
        }

    def __str__(self):
        return f"Object '{self.name}', id: {self.id}, pos: {self.transformation.pos.to_tuple()}"

    def __repr__(self):
        return str(self)
