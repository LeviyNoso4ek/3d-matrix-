from vec import Vec3
import math

class Camera():
    def __init__(self, pos: Vec3):
        self.pos = pos
        self.fov = 30.0
        self.scale = math.tan(math.radians(self.fov * 0.5))
        self.forward = Vec3(0, 0, 1).norm()

        self.up = Vec3(0, 1, 0) 