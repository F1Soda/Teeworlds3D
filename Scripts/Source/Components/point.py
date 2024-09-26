import Scripts.Source.Components.component as component_m
import Scripts.Source.Render.gizmos as gizmos_m
import glm

NAME = "Point"
DESCRIPTION = "Responsible for rendering point"


class Point(component_m.Component):
    def __init__(self, color, size, save_size=True, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self.gizmos_point = gizmos_m.Gizmos.Point(None, glm.vec3(), color, None, size, save_size)

    def update_render_mode(self):
        if self not in self.app.level.opaque_renderer:
            self.app.level.opaque_renderer.append(self)
            # self.app.scene.transparency_renderer.append(self)

    @property
    def color(self):
        return self.gizmos_point.color

    @color.setter
    def color(self, value):
        self.gizmos_point.color = value

    @property
    def size(self):
        return self.gizmos_point.size

    @size.setter
    def size(self, value):
        self.gizmos_point.size = value

    @property
    def save_size(self):
        return self.gizmos_point.save_size

    @save_size.setter
    def save_size(self, value):
        self.gizmos_point.save_size = value

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self.gizmos_point.ctx = app.ctx
        self.gizmos_point.camera = rely_object.level.camera_component

    def apply(self):
        self.gizmos_point.pos = self.rely_object.transformation.pos
        self.gizmos_point.draw()

    def serialize(self) -> {}:
        return {
            "color": ('vec', self.color.to_tuple()),
            "size": self.size,
            "save_size": self.save_size,
            'enable': self.enable
        }

    def delete(self):
        self.gizmos_point.delete()
        super().delete()
