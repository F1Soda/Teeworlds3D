#version 330 core
out vec4 FragColor;

uniform sampler2D texture0;

in vec2 texcoord;

uniform bool depthTexture;

float near = 0.1;
float far  = 1000.0;

float LinearizeDepth(float depth)
{
    float z = depth * 2.0 - 1.0; // back to NDC
    return (2.0 * near * far) / (far + near - z * (far - near));
}

void main()
{
    FragColor = texture(texture0, texcoord);
    if (depthTexture) {
        float linearDepth = LinearizeDepth(FragColor.r);
        FragColor = vec4(vec3((linearDepth - 0.1) / (10 - .1)), 1.0);//;
    }
}