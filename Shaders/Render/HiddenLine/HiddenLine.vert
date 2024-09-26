#version 330

layout (location = 0) in vec3 in_position;


flat out vec3 startPos;
out vec3 vertPos;

uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_proj;


void main()
{
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
    vertPos = gl_Position.xyz / gl_Position.w;
    startPos = vertPos;
}