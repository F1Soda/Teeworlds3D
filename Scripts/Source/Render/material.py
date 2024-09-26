import moderngl
import Scripts.Source.Render.shader_program as shader_program_m
import glm
import enum
import re


class RenderMode(enum.Enum):
    Opaque = 0
    Transparency = 1


class VisibleState(enum.Enum):
    Visible = 0
    Debug = 1


class MaterialProperty:
    def __init__(self, name: str, value, material, visible: VisibleState = 0):
        self.name = name
        self.visible = visible
        self.material = material
        self.value = value

    def __str__(self):
        return f'{self.name}: {self.value}'

    def __repr__(self):
        return str(self)


class Material:
    def __init__(self, ctx: moderngl.Context, material_name: str, shader_program: shader_program_m.ShaderProgram,
                 properties, render_mode=RenderMode.Opaque):
        self.ctx = ctx
        self.name = material_name
        self.shader_program = shader_program
        self.properties = {}
        for name, value in properties:
            self.properties[name] = MaterialProperty(name, value, self)

        # Camera
        self.camera_component = None
        self.camera_transformation = None
        self.render_mode = render_mode

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key].value = value
        self.shader_program[key].write(value)

    def initialize(self):
        self._initialize_shader_with_base_uniforms()

    def _initialize_shader_with_base_uniforms(self):
        # Projection Matrix
        m_proj = self.shader_program.get('m_proj')
        if m_proj:
            m_proj.write(self.camera_component.m_proj)

    def _update_base_uniforms(self, transform_object, light_component):
        # Camera Position
        cam_pos = self.shader_program.get('camPos')
        if cam_pos and self.camera_transformation is not None:
            cam_pos.write(self.camera_transformation.pos)
        # View Matrix
        m_view = self.shader_program.get('m_view')
        if m_view and self.camera_transformation is not None:
            m_view.write(self.camera_component.m_view)
        # Model Matrix
        m_matrix = self.shader_program.get('m_model')
        if m_matrix:
            m_matrix.write(transform_object.m_model)
        # Light
        light_position = self.shader_program.get("light.position")
        light_Ia = self.shader_program.get("light.Ia")
        light_Id = self.shader_program.get("light.Id")
        light_Is = self.shader_program.get("light.Is")
        if light_component:
            # light_position
            if light_position:
                light_position.write(light_component.transformation.pos)
            # light_Ia
            if light_Ia:
                light_Ia.write(light_component.intensity_ambient)
            # light_Id
            if light_Id:
                light_Id.write(light_component.intensity_diffuse)
            # light_Is
            if light_Is:
                light_Is.write(light_component.intensity_specular)
        else:
            if light_position:
                light_position.write(glm.vec3())
            # light_Ia
            if light_Ia:
                light_Ia.write(glm.vec3())
            # light_Id
            if light_Id:
                light_Id.write(glm.vec3())
            # light_Is
            if light_Is:
                light_Is.write(glm.vec3())

    def _update_properties_uniforms(self):
        for key, value in self.properties.items():
            if key.startswith('tex'):
                p = self.shader_program.get(key)
                if p:
                    location = int(re.search(r'(?<=_)\d+', key).group())
                    value.value.use(location=location)
                    self.shader_program[key] = location
                    continue
            p = self.shader_program.get(key)
            if p:
                if isinstance(value.value, bool):
                    self.shader_program[key] = value.value
                    continue
                p.write(value.value)
            pass

    def update_projection_matrix(self, m_proj):
        if self.shader_program.get('m_proj'):
            self.shader_program.get('m_proj').write(m_proj)

    def update(self, transform_object, light_component):
        self._update_base_uniforms(transform_object, light_component)
        self._update_properties_uniforms()

    def destroy(self):
        self.ctx = None
        self.shader_program.destroy()
        self.shader_program = None
        for shader_property in self.properties:
            shader_property._material = None
            shader_property.value = None

    def __str__(self):
        return f"Material {self.name}. Props: {self.properties}"

    def __repr__(self):
        return str(self)
