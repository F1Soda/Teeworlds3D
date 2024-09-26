#version 330 core

uniform vec4 color;
uniform sampler2D texture_0;

out vec4 FragColor;

in vec2 TexCoords;

void main()
{
    FragColor = texture(texture_0, TexCoords) * color;
}