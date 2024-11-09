import numpy as np
import Scripts.Source.General.utils as utils_m
import Scripts.Source.Render.render as render
import Scripts.Source.General.Game.teeworlds as main_m
import glm
import pygame as pg
import moderngl as mgl

meshes = dict()
materials = dict()
shader_programs = dict()
vaos = dict()
textures = dict()


def _init_cube(ctx):
    vertices = [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5),
                (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5)]

    indices = [(0, 2, 3), (0, 1, 2),
               (1, 7, 2), (1, 6, 7),
               (6, 5, 4), (4, 7, 6),
               (3, 4, 5), (3, 5, 0),
               (3, 7, 4), (3, 2, 7),
               (0, 6, 1), (0, 5, 6)]

    outline_indices = [(0, 1), (1, 2), (2, 3), (3, 0),
                       (0, 5), (5, 4), (4, 3),
                       (4, 7), (7, 2),
                       (5, 6), (6, 1),
                       (6, 7)
                       ]

    tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
    tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                         (0, 2, 3), (0, 1, 2),
                         (0, 1, 2), (2, 3, 0),
                         (2, 3, 0), (2, 0, 1),
                         (0, 2, 3), (0, 1, 2),
                         (3, 1, 2), (3, 0, 1)]
    normals = [(0, 0, 1) * 6,
               (1, 0, 0) * 6,
               (0, 0, -1) * 6,
               (-1, 0, 0) * 6,
               (0, 1, 0) * 6,
               (0, -1, 0) * 6, ]

    mesh = render.Mesh(ctx, "cube", '3f 2f 3f', ['in_position', 'in_texCoord', 'in_normal'])
    mesh.vertices = [glm.vec3(vertice) for vertice in vertices]
    mesh.indices = indices
    mesh.triangle_vertices = utils_m.get_data_elements_by_indices(vertices, indices)
    mesh.tex_coord = utils_m.get_data_elements_by_indices(tex_coord, tex_coord_indices)
    mesh.normals = np.array(normals, dtype='f4').reshape(36, 3)
    mesh.hidden_vertices = utils_m.get_data_elements_by_indices(vertices, outline_indices)
    return mesh


def _init_tetrahedron(ctx):
    temp = -glm.sqrt(3) / 24 * (8 * glm.sqrt(2) - 9)
    vertices = [
        glm.vec3(glm.sqrt(3) / 3, temp, 0),
        glm.vec3(-glm.sqrt(3) / 6, temp, 0.5),
        glm.vec3(-glm.sqrt(3) / 6, temp, -0.5),
        glm.vec3(0, glm.sqrt(3) * 3 / 8, 0)
    ]

    indices = [
        (0, 1, 2),  # Face 1
        (0, 2, 3),  # Face 2
        (0, 3, 1),  # Face 3
        (1, 3, 2)  # Face 4
    ]

    # Currently tex coordinates are wrong

    tex_coord = [
        (0, 0),  # TexCoord 0
        (1, 0),  # TexCoord 1
        (1, 1),  # TexCoord 2
        (0, 1)  # TexCoord 3
    ]

    tex_coord_indices = [
        (0, 1, 2),  # Face 1
        (0, 1, 3),  # Face 2
        (0, 2, 3),  # Face 3
        (1, 2, 3)  # Face 4
    ]

    outline_indices = [
        (0, 1), (1, 2), (2, 0),
        (1, 3), (3, 0),
        (2, 3)
    ]

    normals = [
        (0, -1, 0) * 3,  # Normal for Face 1
        (-vertices[1].x, -vertices[1].y, -vertices[1].z) * 3,
        (-vertices[2].x, -vertices[2].y, -vertices[2].z) * 3,
        (-vertices[0].x, -vertices[0].y, -vertices[0].z) * 3
    ]
    mesh = render.Mesh(ctx, "tetrahedron", '3f 2f 3f', ['in_position', 'in_texCoord', 'in_normal'])
    mesh.indices = indices
    mesh.vertices = [glm.vec3(vertice) for vertice in vertices]
    mesh.triangle_vertices = utils_m.get_data_elements_by_indices(vertices, indices)
    mesh.tex_coord = utils_m.get_data_elements_by_indices(tex_coord, tex_coord_indices)
    mesh.normals = np.array(normals, dtype='f4').reshape(12, 3)
    mesh.hidden_vertices = utils_m.get_data_elements_by_indices(vertices, outline_indices)
    return mesh


def _init_octahedron(ctx):
    vertices = [
        (-0.5, 0, -0.5), (-0.5, 0, 0.5), (0.5, 0, 0.5), (0.5, 0, -0.5), (0, glm.sqrt(2) / 2, 0),
        (0, -glm.sqrt(2) / 2, 0)
    ]

    indices = [
        (0, 1, 4),  # Face 1
        (1, 2, 4),  # Face 2
        (2, 3, 4),  # Face 3
        (3, 0, 4),
        (0, 3, 5),
        (3, 2, 5),
        (2, 1, 5),
        (1, 0, 5),
    ]

    # Currently tex coordinates are wrong

    tex_coord = [
        (0, 0),  # TexCoord 0
        (1, 0),  # TexCoord 1
        (1, 1),  # TexCoord 2
        (0, 1)  # TexCoord 3
    ]

    tex_coord_indices = [
        (0, 1, 2),  # Face 1
        (0, 1, 3),  # Face 2
        (0, 2, 3),  # Face 3
        (1, 2, 3),  # Face 4
        (0, 1, 2),  # Face 1
        (0, 1, 3),  # Face 2
        (0, 2, 3),  # Face 3
        (1, 2, 3),  # Face 4
    ]
    temp_y = 1 / (3 * glm.sqrt(2))

    normals = [
        (-1 / 3, temp_y, 0) * 3,  # Normal for Face 1
        (0, temp_y, 1 / 3) * 3,  # Normal for Face 2
        (1 / 3, temp_y, 0) * 3,  # Normal for Face 3
        (0, temp_y, -1 / 3) * 3,  # Normal for Face 4
        (0, -temp_y, -1 / 3) * 3,  # Normal for Face 1
        (1 / 3, -temp_y, 0) * 3,  # Normal for Face 2
        (0, -temp_y, 1 / 3) * 3,  # Normal for Face 3
        (-1 / 3, -temp_y, 0) * 3  # Normal for Face 4
    ]

    outline_indices = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (0, 4), (1, 4), (2, 4), (3, 4),
        (0, 5), (1, 5), (2, 5), (3, 5)
    ]

    mesh = render.Mesh(ctx, "octahedron", '3f 2f 3f', ['in_position', 'in_texCoord', 'in_normal'])
    mesh.vertices = [glm.vec3(vertice) for vertice in vertices]
    mesh.indices = indices
    mesh.triangle_vertices = utils_m.get_data_elements_by_indices(vertices, indices)
    mesh.tex_coord = utils_m.get_data_elements_by_indices(tex_coord, tex_coord_indices)
    mesh.normals = np.array(normals, dtype='f4').reshape(24, 3)
    mesh.hidden_vertices = utils_m.get_data_elements_by_indices(vertices, outline_indices)
    return mesh


def _init_plane(ctx):
    vertices = [(-0.5, 0, -0.5), (-0.5, 0, 0.5), (0.5, 0, 0.5), (0.5, 0, -0.5)]

    tex_coord = [(0, 0), (0, 1), (1, 1), (1, 0)]

    indices = [(0, 1, 2), (0, 2, 3), (0, 2, 1), (0, 3, 2)]

    normals = [(0, -1, 0)] * 6 + [(0, 1, 0)] * 6

    mesh = render.Mesh(ctx, "plane", '3f 2f 3f', ['in_position', 'in_texCoord', 'in_normal'])
    mesh.vertices = [glm.vec3(vertice) for vertice in vertices]
    mesh.indices = indices
    mesh.triangle_vertices = utils_m.get_data_elements_by_indices(vertices, indices)
    mesh.tex_coord = utils_m.get_data_elements_by_indices(tex_coord, indices)
    mesh.normals = np.array(normals, dtype='f4')
    return mesh


def _init_unlit_material(ctx, color, name, render_mode=render.RenderMode.Opaque):
    return render.Material(ctx, name, shader_programs['unlit'], [('color', glm.vec4(color)),
                                                                 ('tilling', glm.vec2(1)),
                                                                 ('offset', glm.vec2(0)),
                                                                 ('texture_0', textures['white'])], render_mode)


def _init_lit_material(ctx, tint, name):
    return render.Material(ctx, name, shader_programs['lit'], [
        ('tint', glm.vec4(tint)),
        ('tilling', glm.vec2(1)),
        ('offset', glm.vec2(0)),
        ('texture_0', textures['white'])
    ])


def _init_shaders(ctx):
    shader_programs['unlit'] = render.ShaderProgram(ctx, 'Render/Unlit', 'unlit')
    shader_programs['lit'] = render.ShaderProgram(ctx, 'Render/Lit', 'unlit')
    shader_programs['word_axis_gizmo'] = render.ShaderProgram(ctx, 'Render/WordAxisGizmo', 'word_axis_gizmo')
    shader_programs['point_gizmo'] = render.ShaderProgram(ctx, 'Render/PointGizmo', 'point_gizmo')
    shader_programs['segment_gizmo'] = render.ShaderProgram(ctx, 'Render/SegmentGizmo', 'segment_gizmo')
    shader_programs['object_picking'] = render.ShaderProgram(ctx, 'Render/ObjectPicking', 'object_picking')
    shader_programs['silhouette'] = render.ShaderProgram(ctx, 'Render/Silhouette', 'silhouette')
    shader_programs['section'] = render.ShaderProgram(ctx, 'Render/Section', 'section')
    shader_programs['hidden_line'] = render.ShaderProgram(ctx, "Render/HiddenLine", "hidden_line")


def _init_textures(ctx):
    # Default White Color
    texture = pg.image.load('Textures/white.png').convert_alpha()
    texture = ctx.texture(size=texture.get_size(), components=4, data=pg.image.tostring(texture, 'RGBA'))
    textures['white'] = texture

    # Grid
    texture = pg.image.load('Textures/grid.png').convert_alpha()
    texture = ctx.texture(size=texture.get_size(), components=4, data=pg.image.tostring(texture, 'RGBA'))
    texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR_MIPMAP_LINEAR)
    texture.build_mipmaps()
    texture.anisotropy = 32.0

    textures['grid'] = texture




def get_segment_vao(ctx, start, end):
    buffer_format = '3f'
    data = np.array([start, end], dtype='f4')
    vbo = ctx.buffer(data)
    vao = ctx.vertex_array(shader_programs['word_axis_gizmo'].bin_program,
                           [(vbo, buffer_format, 'in_position')])
    return vao


def get_point_vao(ctx):
    buffer_format = '1f'
    data = np.array([0], dtype='f4')  # Provide a dummy value
    vbo = ctx.buffer(data)
    vao = ctx.vertex_array(shader_programs['point_gizmo'].bin_program,
                           [(vbo, buffer_format, 'dumpy_input')])
    return vao


def _init_vaos(ctx):
    vaos['point'] = get_point_vao(ctx)


def init(ctx):
    _init_shaders(ctx)
    _init_textures(ctx)
    _init_vaos(ctx)
    # Meshes
    meshes['cube'] = _init_cube(ctx)
    meshes['plane'] = _init_plane(ctx)
    meshes['tetrahedron'] = _init_tetrahedron(ctx)
    meshes['octahedron'] = _init_octahedron(ctx)

    # Materials
    # Unlit
    materials['red_unlit'] = _init_unlit_material(ctx, (1, 0, 0, 1), 'red_unlit')
    materials['orange_unlit'] = _init_unlit_material(ctx, (1, 0.6, 0, 1), 'orange_unlit')
    materials['green_unlit'] = _init_unlit_material(ctx, (0, 1, 0, 1), 'green_unlit')
    materials['blue_unlit'] = _init_unlit_material(ctx, (0, 0, 1, 1), 'blue_unlit')
    materials['magenta_unlit'] = _init_unlit_material(ctx, (1, 0, 1, 1), 'magenta_unlit')
    materials['cyan_unlit'] = _init_unlit_material(ctx, (0, 1, 1, 1), 'cyan_unlit')
    materials['gray_unlit'] = _init_unlit_material(ctx, (0.5, 0.5, 0.5, 1), 'gray_unlit')
    materials['black_unlit'] = _init_unlit_material(ctx, (0, 0, 0, 1), 'black_unlit')
    materials['white_unlit'] = _init_unlit_material(ctx, (1, 1, 1, 1), 'white_unlit')

    materials['transparency_white_unlit'] = _init_unlit_material(ctx, (1, 1, 1, 0.5), 'transparency_white_unlit',
                                                                 render.RenderMode.Transparency)

    materials['transparency_gray_unlit'] = _init_unlit_material(ctx, (0.5, 0.5, 0.5, 0.5), 'transparency_gray_unlit',
                                                                render.RenderMode.Transparency)

    # Lit
    materials['red_lit'] = _init_lit_material(ctx, (1, 0, 0, 1), 'red_lit')
    materials['orange_lit'] = _init_lit_material(ctx, (1, 0.6, 0, 1), 'orange_lit')
    materials['green_lit'] = _init_lit_material(ctx, (0, 1, 0, 1), 'green_lit')
    materials['blue_lit'] = _init_lit_material(ctx, (0, 0, 1, 1), 'blue_lit')
    materials['gray_lit'] = _init_lit_material(ctx, (0.5, 0.5, 0.5, 1), 'gray_lit')

    # Section (lit but for Section component)
    materials['section'] = render.Material(ctx, 'section', shader_programs['section'], [
        ('tint', glm.vec4(0.1, 1, 0.5, 1)),
        ('tilling', glm.vec2(1)),
        ('offset', glm.vec2(0)),
        ('texture_0', textures['white']),
        ('texture_1', textures['white']),
        ('winSize', glm.vec2(main_m.WIN_SIZE[0], main_m.WIN_SIZE[1])),
        ('inverse', False)
    ])

    # Special
    materials['grid'] = render.Material(ctx, "Grid", shader_programs['unlit'], [
        ('color', glm.vec4(1)),
        ('tilling', glm.vec2(1)),
        ('offset', glm.vec2(0)),
        ('texture_0', textures['grid'])
    ], render.RenderMode.Transparency)
    materials['object_picking'] = render.Material(ctx, "Object Picking", shader_programs['object_picking'],
                                                  [('color', glm.vec4(0))])
