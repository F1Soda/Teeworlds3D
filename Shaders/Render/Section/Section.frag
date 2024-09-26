#version 330 core

layout (location = 0) out vec4 fragColor;

in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D texture_0;
uniform sampler2D texture_1;
uniform bool inverse;
uniform vec3 camPos;
uniform vec4 tint;
uniform vec2 tilling;
uniform vec2 offset;
uniform vec2 winSize;

vec3 getLight(vec3 color)
{
    vec3 normal = normalize(normal);
    vec3 ambient = light.Ia;

    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, normal));
    vec3 diffuse = diff * light.Id;

    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, normal);
    vec3 specular = pow(max(dot(viewDir, reflectDir), 0), 32) * light.Is;


    return color * (ambient + diffuse + specular);
}

void main() {
    float silhouette_value0 = texture(texture_0, gl_FragCoord.xy / winSize).r;
    float silhouette_value1 = texture(texture_1, gl_FragCoord.xy / winSize).r;
    if (inverse) {
        if (silhouette_value0 != silhouette_value1) {
            discard;
        }
    }
    else {
        if (silhouette_value0 == silhouette_value1) {
            discard;
        }
    }
    float gamma = 2.2;
    vec3 color = tint.rgb;
    color = pow(color, vec3(gamma));

    color = getLight(color);

    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1);
}