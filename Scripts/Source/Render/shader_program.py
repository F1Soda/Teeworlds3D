class ShaderProgram:
    def __init__(self, ctx, folder_name, name):
        self.ctx = ctx
        self.name = name
        self.bin_program = self.get_bin_program(folder_name)

    def __getitem__(self, item):
        return self.bin_program[item]

    def __setitem__(self, key, value):
        self.bin_program[key] = value

    def get_bin_program(self, shader_folder: str):
        shader_name = shader_folder.split('/')[-1]
        with open(f'Shaders/{shader_folder}/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'Shaders/{shader_folder}/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def get(self, key: str):
        return self.bin_program.get(key, None)

    def destroy(self):
        self.bin_program.release()
        self.ctx = None
