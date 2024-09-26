#version 330 core

out vec4 fragColor;

uniform sampler2D texture_0;
uniform vec4 color;
uniform vec2 tilling;
uniform vec2 offset;

in vec2 texCoord;

void main() {
    vec2 texCoord = texCoord* tilling + offset;
    vec4 textureColor = texture(texture_0, texCoord);
    fragColor = textureColor * color;
}