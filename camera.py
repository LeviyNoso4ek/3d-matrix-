from vec import Vec3
from funcs import clamp
from matrix import *
import math

class Camera():
    def __init__(self, pos: Vec3):
        self.P = pos
        
        self.world_up = Vec3(0, 1, 0)
        
        self.yaw = -90.0
        self.pitch = 0.0
        
        self.F = Vec3()
        self.R = Vec3() 
        self.U = Vec3()
        
        self.fov = 90.0
        self.scale = math.tan(math.radians(self.fov * 0.5))
        
        self.update_basis()
    def update_basis(self):
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)
        
        forward = Vec3(
            math.cos(pitch_rad) * math.cos(yaw_rad),
            math.sin(pitch_rad),
            math.cos(pitch_rad) * math.sin(yaw_rad),
        )
        
        self.F = forward.norm()
        self.R = self.F.cross(self.world_up).norm()
        self.U = self.R.cross(self.F).norm()
    def rot(self, delta_yaw, delta_pitch):
        self.yaw += delta_yaw
        self.pitch = clamp(self.pitch + delta_pitch, -89.0, 89.0)
        
        self.update_basis()
    def get_v_matrix(self):
        return Matrix(data=[
            [self.R.x,   self.R.y,  self.R.z, -self.P.dot(self.R)],
            [self.U.x,   self.U.y,  self.U.z, -self.P.dot(self.U)],
            [-self.F.x, -self.F.y, -self.F.z,  self.P.dot(self.F)],
            [    0,         0,         0,              1         ]
        ])