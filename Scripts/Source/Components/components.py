import Scripts.Source.Components.Default.transformation as transformation_m
import Scripts.Source.Components.Default.renderer as renderer_m
import Scripts.Source.Components.Default.camera as camera_m
import Scripts.Source.Components.Default.light as light_m
import Scripts.Source.Components.Default.free_fly_move as free_fly_move_m
import Scripts.Source.Components.Default.point as point_m
import Scripts.Source.Components.Default.segment as segment_m
import Scripts.Source.Components.Default.plane as plane_m
import Scripts.Source.Components.Default.secateur as secateur_m
import Scripts.Source.Components.Default.section as section_m
import Scripts.Source.Components.Custom.translator as translator_m
import Scripts.Source.Components.Custom.rotator as rotator_m
import Scripts.Source.Components.Custom.Player.fps_camera_movement as fps_camera_movement_m
import Scripts.Source.Components.Custom.Player.player as player_m
import Scripts.Source.Components.Custom.Player.player_controller as player_controller_m
import Scripts.Source.Components.Default.rigidbody as rigidbody_m
import Scripts.Source.Components.Default.Colliders.collider as collider_m
import Scripts.Source.Components.Default.Colliders.mesh_collider as mesh_collider_m
import Scripts.Source.Components.Custom.debug as debug_m
import Scripts.Source.Components.Default.mesh_filter as mesh_filter_m
import Scripts.Source.Components.Default.Colliders.box_collider as box_collider_m
import Scripts.Source.Components.Custom.Player.ground_checker as ground_checker_m

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
FPSCameraMovement = fps_camera_movement_m.FPSCameraMovement
Player = player_m.Player
PlayerController = player_controller_m.PlayerController
RigidBody = rigidbody_m.RigidBody
Collider = collider_m.Collider
MeshCollider = mesh_collider_m.MeshCollider
BoxCollider = box_collider_m.BoxCollider
MeshFilter = mesh_filter_m.MeshFilter
GroundChecker = ground_checker_m.GroundChecker

Debug = debug_m.Debug

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
    "Rotator": Rotator,
    "FPSCameraMovement": FPSCameraMovement,
    "Player": Player,
    "PlayerController": PlayerController,
    "RigidBody": RigidBody,
    "Collider": Collider,
    "Mesh Collider": MeshCollider,
    "Box Collider": BoxCollider,
    "Mesh Filter": MeshFilter,
    "Ground Checker": GroundChecker
}
