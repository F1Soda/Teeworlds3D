# Reserved id:
# 1 — camera
# 2-4 — transformation axis
# 5-... — scene objects

class IndexManager:
    def __init__(self):
        self.global_index = 1
        self.unused_indices = []

    def get_id(self):
        id = self.global_index
        self.global_index += 1
        return id

    @staticmethod
    def get_color_by_id(id: int):
        if id > 255 * 255 * 255:
            return 1, 1, 1
        r = id % 255
        g = (id // 255) % 255
        b = ((id // 255) // 255) % 255
        # print(r,g,b)
        # print(hex(r),hex(g),hex(b))
        return r / 255.0, g / 255.0, b / 255.0

        # OLD
        # t = id / 255
        # r, g, b = 0, 0, 0
        # if t < 1:
        #     r = t
        # if 1 <= t < 2:
        #     r = 1
        #     g = (id - 255) / 255
        # if 2 <= t:
        #     r, g = 1, 1
        #     b = min((id - 255 * 2) / 255, 1)
        # return r, g, b

    @staticmethod
    def get_id_by_color(color: tuple):
        r = color[0]  # int(color[0], 16)
        g = color[1]  # int(color[1], 16)
        b = color[2]  # int(color[2], 16)
        # print(r, g, b)
        return r + g * 255 + b * 255 * 255

        # OLD
        # return color[0] * 255 + color[1] * 255 + color[2] * 255

    def serialize(self):
        return {
            'global_index': self.global_index,
            'unused_indices': self.unused_indices
        }
