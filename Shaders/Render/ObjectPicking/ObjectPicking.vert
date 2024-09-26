#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec2 in_texCoord;
layout (location = 2) in vec3 in_normal;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;


void main() {
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
    vec3 temp = in_normal;
    vec2 temp_1 = in_texCoord;
}