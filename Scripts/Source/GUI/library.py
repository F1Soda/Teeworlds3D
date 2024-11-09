import Scripts.Source.General.utils as utils
import Scripts.Source.Render.shader_program as shader_program_m
import pygame as pg
import moderngl as mgl

primitives_vao = dict()
shader_programs = dict()
textures = dict()


def _inti_shader_programs(ctx):
    shader_programs['BlockGUI'] = shader_program_m.ShaderProgram(ctx, 'GUI/BlockGUI', 'BlockGUI')
    shader_programs['TextGUI'] = shader_program_m.ShaderProgram(ctx, 'GUI/TextGUI', 'TextGUI')
    shader_programs['TextureGUI'] = shader_program_m.ShaderProgram(ctx, 'GUI/TextureGUI', 'TextureGUI')


def _inti_primitives(ctx):
    # Quad for Block
    buffer_format = '2f'
    vertices = [(0, 0), (0, 1), (1, 1), (1, 0)]
    indices = [(0, 2, 1), (0, 3, 2)]
    data = utils.get_data_elements_by_indices(vertices, indices)
    vbo = ctx.buffer(data)
    vao = ctx.vertex_array(shader_programs['BlockGUI'].bin_program, [(vbo, buffer_format, 'inPosition')])
    primitives_vao['quad'] = vao

    # Quad for Text
    buffer_format = '2f'
    vbo = ctx.buffer(data)
    vao = ctx.vertex_array(shader_programs['TextGUI'].bin_program, [(vbo, buffer_format, 'inPosition')])
    primitives_vao['text_quad'] = vao

    # Quad for Texture
    buffer_format = '2f'
    vbo = ctx.buffer(data)
    vao = ctx.vertex_array(shader_programs['TextureGUI'].bin_program, [(vbo, buffer_format, 'inPosition')])
    primitives_vao['textured_quad'] = vao


def _init_textures(ctx):
    # Font
    texture = pg.image.load('Textures/Verdana_B_alpha.png').convert_alpha()
    texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
    texture = ctx.texture(size=texture.get_size(), components=4, data=pg.image.tostring(texture, 'RGBA'))
    texture.filter = (mgl.NEAREST, mgl.NEAREST)
    textures['font'] = texture

    texture = pg.image.load('Textures/Verdana_with_boundaries.png').convert_alpha()
    texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
    texture = ctx.texture(size=texture.get_size(), components=4, data=pg.image.tostring(texture, 'RGBA'))
    texture.filter = (mgl.NEAREST, mgl.NEAREST)
    textures['font_boundaries'] = texture

    # Crosshair
    texture = pg.image.load('Textures/aim.png').convert_alpha()
    texture = ctx.texture(size=texture.get_size(), components=4, data=pg.image.tostring(texture, 'RGBA'))

    textures['crosshair'] = texture


def init(ctx):
    _inti_shader_programs(ctx)
    _inti_primitives(ctx)
    _init_textures(ctx)
