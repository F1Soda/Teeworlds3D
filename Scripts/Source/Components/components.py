import Scripts.Source.Components.transformation as transformation_m
import Scripts.Source.Components.renderer as renderer_m
import Scripts.Source.Components.camera as camera_m
import Scripts.Source.Components.light as light_m
import Scripts.Source.Components.free_fly_move as free_fly_move_m
import Scripts.Source.Components.point as point_m
import Scripts.Source.Components.segment as segment_m
import Scripts.Source.Components.plane as plane_m
import Scripts.Source.Components.secateur as secateur_m
import Scripts.Source.Components.section as section_m
import Scripts.Source.Components.translator as translator_m
import Scripts.Source.Components.rotator as rotator_m

Transformation = transformation_m.Transformation
Renderer = renderer_m.Renderer
Camera = camera_m.Camera
Light = light_m.Light
FreeFlyMove = free_fly_move_m.FreeFlyMove
Point = point_m.Point
Segment = segment_m.Segment
Plane = plane_m.Plane
Secateur = secateur_m.Secateur
Section = section_m.Section
Translator = translator_m.Translator
Rotator = rotator_m.Rotator

components = {
    "Transformation": Transformation,
    "Renderer": Renderer,
    "Camera": Camera,
    "Light": Light,
    "FreeFlyMove": FreeFlyMove,
    "Point": Point,
    "Segment": Segment,
    "Plane": Plane,
    "Secateur": Secateur,
    "Section": Section,
    "Translator": Translator,
    "Rotator": Rotator
}
