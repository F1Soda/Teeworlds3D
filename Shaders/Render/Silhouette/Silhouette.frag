#version 330

layout (location = 0) out vec4 fragColor;

uniform bool subtract;
uniform bool toBackground;


void main() {
    if (subtract) {
        fragColor = vec4(0, 0, 0, 1.0);
    }
    else {
        fragColor = vec4(1.0, 0, 0, 1.0);
    }
}