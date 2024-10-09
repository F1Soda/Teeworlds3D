import glm

class GameObject:
    def __init__(self, name):
        self.name = name
        self._rot = glm.vec3(0.0, 0.0, 0.0)
        self._pos = glm.vec3(0.0, 0.0, 0.0)
        self._forward = glm.vec3(0.0, 0.0, -1.0)
        self._right = glm.vec3(1.0, 0.0, 0.0)
        self._up = glm.vec3(0.0, 1.0, 0.0)
        self.children = []
        self.m_r = glm.mat4(1.0)  # Identity matrix

    @property
    def rot(self):
        return self._rot

    @rot.setter
    def rot(self, value):
        if isinstance(value, tuple):
            value = glm.vec3(*value)
        diff = value - self._rot
        self._rot = value

        self.update_model_matrix()

        self._forward = glm.normalize(glm.vec3(self.m_r[0][2], self.m_r[1][2], self.m_r[2][2]))
        self._right = glm.normalize(glm.vec3(self.m_r[0][0], self.m_r[1][0], self.m_r[2][0]))
        self._up = glm.normalize(glm.vec3(self.m_r[0][1], self.m_r[1][1], self.m_r[2][1]))

        # Apply the rotation to child objects
        for child in self.children:
            if child.name != "Game Camera":
                child.apply_parent_rotation(self.m_r)

    def update_model_matrix(self):
        x, y, z = glm.radians(self._rot.x), glm.radians(self._rot.y), glm.radians(self._rot.z)

        # Rotation matrices for pitch, yaw, and roll
        R_pitch = glm.mat4(1.0)
        R_pitch = glm.rotate(R_pitch, x, glm.vec3(1.0, 0.0, 0.0))

        R_yaw = glm.mat4(1.0)
        R_yaw = glm.rotate(R_yaw, y, glm.vec3(0.0, 1.0, 0.0))

        R_roll = glm.mat4(1.0)
        R_roll = glm.rotate(R_roll, z, glm.vec3(0.0, 0.0, 1.0))

        # Combine the rotation matrices
        self.m_r = R_pitch * R_yaw * R_roll

    def apply_parent_rotation(self, parent_rotation_matrix):
        # Apply the parent's rotation to the child's position
        self._pos = glm.vec3(parent_rotation_matrix * glm.vec4(self._pos, 1.0))

        # Apply the parent's rotation to the child's rotation
        child_quat = glm.quat(glm.radians(self._rot))
        combined_quat = parent_rotation_matrix * glm.mat4_cast(child_quat)
        #self._rot = glm.degrees(glm.eulerAngles(glm.quat_cast(combined_quat)))

# Example usage
parent = GameObject("Parent")
child = GameObject("Child")
child._pos = glm.vec3(0,0,-1)
parent.children.append(child)


parent.rot = (90, 0, 0)  # Rotate the parent by 45 degrees around X, 30 degrees around Y, and 15 degrees around Z

print("Parent forward vector:", parent._forward)
print("Parent right vector:", parent._right)
print("Parent up vector:", parent._up)
print()
print("Child position:", child._pos)
print("Child rotation:", child._rot)
print("Child forward vector:", child._forward)
print("Child right vector:", child._right)
print("Child up vector:", child._up)