import glm

FLT_MAX = 10 ** 9
GJK_EPA_MAX_ITER = 32


class Simplex:
    def __init__(self):
        self.points = []

    def append(self, point):
        self.points.append(point)

    def __getitem__(self, index):
        return self.points[index]

    def __setitem__(self, index, point):
        self.points[index] = point

    def __str__(self):
        return f"Simplex with {len(self.points)} points"

    def __repr__(self):
        return self.__str__()


class CollisionPoint:
    def __init__(self, normal, penetration_depth):
        self.normal = normal
        self.depth = penetration_depth


def _case_line(simplex, direction):
    a = simplex[0]
    b = simplex[1]
    ab = b - a
    ao = - a
    if same_direction_vec(ab, ao):
        direction = glm.cross(glm.cross(ab, ao), ab)
    else:
        simplex.points = [a]
        direction = ao
    return direction


def _case_triangle(simplex, direction):
    a = simplex[0]
    b = simplex[1]
    c = simplex[2]

    ab = b - a
    ac = c - a
    ao = -a

    abc = glm.cross(ab, ac)

    if same_direction_vec(glm.cross(abc, ac), ao):
        if same_direction_vec(ac, ao):
            simplex.points = [a, c]
            direction = glm.cross(glm.cross(ac, ao), ac)
        else:
            simplex.points = [a, b]
            return _case_line(simplex, direction)
    else:
        if same_direction_vec(glm.cross(ab, abc), ao):
            simplex.points = [a, b]
            return _case_line(simplex, direction)
        else:
            if same_direction_vec(abc, ao):
                direction = abc
            else:
                simplex.points = [a, c, b]
                direction = -abc
    return direction


def _case_tetrahedron(simplex, direction):
    a = simplex[0]
    b = simplex[1]
    c = simplex[2]
    d = simplex[3]

    ab = b - a
    ac = c - a
    ad = d - a
    ao = -a

    abc = glm.cross(ab, ac)
    acd = glm.cross(ac, ad)
    adb = glm.cross(ad, ab)

    if same_direction_vec(abc, ao):
        simplex.points = [a, b, c]
        return False, _case_triangle(simplex, direction)
    if same_direction_vec(acd, ao):
        simplex.points = [a, c, d]
        return False, _case_triangle(simplex, direction)
    if same_direction_vec(adb, ao):
        simplex.points = [a, d, b]
        return False, _case_triangle(simplex, direction)

    return True, direction


def support(collider_a, collider_b, direction):
    return collider_a.find_furthest_point(direction) - collider_b.find_furthest_point(-direction)


def same_direction_vec(v1, v2):
    return glm.dot(v1, v2) > 0


def _get_face_normals_and_min_triangle(polytope, faces):
    normals = []
    min_triangle = 0
    min_distance = FLT_MAX

    for i in range(0, len(faces), 3):
        a = polytope[faces[i]]
        b = polytope[faces[i + 1]]
        c = polytope[faces[i + 2]]

        normal = glm.normalize(glm.cross(b - a, c - a))
        distance = glm.dot(normal, a)

        if distance < 0:
            normal *= -1
            distance *= -1

        normals.append(glm.vec4(normal, distance))
        if distance < min_distance:
            min_triangle = i // 3
            min_distance = distance

    return normals, min_triangle


def _add_if_unique_edge(edges: list, faces, a, b):
    reverse = None
    for edge in edges:
        if edge == (faces[b], faces[a]):
            reverse = edge
            break

    if reverse is not None:
        edges.remove(reverse)
    else:
        edges.append((faces[a], faces[b]))


def gjk(collider_a, collider_b):
    support_point = support(collider_a, collider_b, glm.vec3(1))
    simplex = Simplex()
    simplex.append(support_point)
    direction = -support_point

    iterations = 0
    while iterations < GJK_EPA_MAX_ITER:
        iterations += 1
        support_point = support(collider_a, collider_b, direction)

        if glm.dot(support_point, direction) <= 0:
            return None

        simplex.points.insert(0, support_point)

        if len(simplex.points) == 2:
            direction = _case_line(simplex, direction)
        elif len(simplex.points) == 3:
            direction = _case_triangle(simplex, direction)
        elif len(simplex.points) == 4:
            collide, direction = _case_tetrahedron(simplex, direction)
            if collide:
                return simplex
        else:
            raise Exception("Invalid simplex dimension")

    return None


def epa(simplex, collider_a, collider_b) -> CollisionPoint | None:
    polytope = [x for x in simplex.points]
    faces = [
        0, 1, 2,
        0, 3, 1,
        0, 2, 3,
        1, 3, 2
    ]
    normals, min_face = _get_face_normals_and_min_triangle(polytope, faces)

    min_normal = glm.vec3()
    min_distance = FLT_MAX

    iterations = 0
    while min_distance == FLT_MAX:
        min_normal = normals[min_face].xyz
        min_distance = normals[min_face].w

        if iterations > GJK_EPA_MAX_ITER:
            break

        iterations += 1

        support_point = support(collider_a, collider_b, min_normal)
        s_distance = glm.dot(min_normal, support_point)

        if abs(s_distance - min_distance > 0.001):
            min_distance = FLT_MAX

            unique_edges = []

            i = 0
            while i < len(normals):
                if same_direction_vec(normals[i].xyz, support_point):
                    f = i * 3

                    _add_if_unique_edge(unique_edges, faces, f, f + 1)
                    _add_if_unique_edge(unique_edges, faces, f + 1, f + 2)
                    _add_if_unique_edge(unique_edges, faces, f + 2, f)

                    faces[f + 2] = faces[-1]
                    faces[f + 1] = faces[-2]
                    faces[f] = faces[-3]
                    faces = faces[:-3]

                    normals[i] = normals[-1]
                    normals.pop()

                    i -= 1
                i += 1

            if len(unique_edges) == 0:
                break

            new_faces = []
            for edge_index_1, edge_index_2 in unique_edges:
                new_faces.append(edge_index_1)
                new_faces.append(edge_index_2)
                new_faces.append(len(polytope))

            polytope.append(support_point)

            new_normals, new_min_face = _get_face_normals_and_min_triangle(polytope, new_faces)

            new_min_distance = FLT_MAX
            for i in range(len(normals)):
                if normals[i].w < new_min_distance:
                    new_min_distance = normals[i].w
                    min_face = i

            if new_normals[new_min_face].w < new_min_distance:
                min_face = new_min_face + len(normals)

            faces += new_faces
            normals += new_normals

    if min_distance == FLT_MAX:
        return None

    return CollisionPoint(min_normal, min_distance + 0.001)


