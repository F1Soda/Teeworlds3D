#version 330 core

in float dumpy_input;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform vec3 position;

void main() {
    float dumpy = dumpy_input;
    gl_Position = m_proj * m_view  * (vec4(position, 1.0));
}