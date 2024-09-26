#version 330

flat in vec3 startPos;
in vec3 vertPos;

out vec4 fragColor;

uniform vec2 resolution;
uniform float dashSize;
uniform float gapSize;
uniform bool dashed;

void main()
{
    vec2 dir = (vertPos.xy - startPos.xy) * resolution / 2.0;
    float dist = length(dir);

    if (dashed && fract(dist / (dashSize + gapSize)) > dashSize / (dashSize + gapSize)) {
        discard;
    }
    fragColor = vec4(1.0);
}