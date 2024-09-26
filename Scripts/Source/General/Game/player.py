import glm

class Player():
    def __init__(self, app):
        self.pos = glm.vec3()
        self.app = app
        self.health = 100

    def delete(self):
        self.app = None
