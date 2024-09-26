#version 330 core

layout (location = 0) in vec2 inPosition;

uniform mat4x4 m_gui;
uniform float letter_size;
uniform vec2 offset;

out vec2 TexCoords;

void main()
{
    vec4 position_VS = m_gui * vec4(inPosition, 0, 1);
    gl_Position = vec4(position_VS.x * 2 - 1, position_VS.y * 2 - 1, 0, 1);
    TexCoords = inPosition / letter_size + offset;
}