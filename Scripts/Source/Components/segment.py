import Scripts.Source.Components.component as component_m
import Scripts.Source.Render.gizmos as gizmos_m
import Scripts.Source.General.Game.object as object_m
import glm

NAME = "Segment"
DESCRIPTION = "Responsible for rendering segment"


class Segment(component_m.Component):
    def __init__(self, p1: object_m.Object, p2: object_m.Object, color: glm.vec4, size, save_size=True, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self.gizmos_segment = gizmos_m.Gizmos.SegmentByPoints(None, p1, p2, color, None, size, save_size)

    def update_render_mode(self):
        if self not in self.app.level.opaque_renderer:
            self.app.level.opaque_renderer.append(self)

    @property
    def p1(self):
        return self.gizmos_segment.p1

    @p1.setter
    def p1(self, value):
        self.gizmos_segment.p1 = value

    @property
    def p2(self):
        return self.gizmos_segment.p2

    @p2.setter
    def p2(self, value):
        self.gizmos_segment.p2 = value

    @property
    def color(self):
        return self.gizmos_segment.color

    @color.setter
    def color(self, value):
        self.gizmos_segment.color = value

    @property
    def size(self):
        return self.gizmos_segment.size

    @size.setter
    def size(self, value):
        self.gizmos_segment.size = value

    @property
    def save_size(self):
        return self.gizmos_segment.save_size

    @save_size.setter
    def save_size(self, value):
        self.gizmos_segment.save_size = value

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self.gizmos_segment.init(self.app.ctx)
        self.gizmos_segment.ctx = app.ctx
        self.gizmos_segment.camera_component = rely_object.level.camera_component

    def apply(self):
        self.gizmos_segment.draw()

    def serialize(self) -> {}:
        return {
            "p1": ('id', self.p1.id),
            "p2": ('id', self.p2.id),
            "color": ('vec', self.color.to_tuple()),
            "size": self.size,
            "save_size": self.save_size,
            'enable': self.enable
        }

    def delete(self):
        self.gizmos_segment.delete()
        super().delete()
