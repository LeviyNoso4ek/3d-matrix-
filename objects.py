import pygame as pg
from camera import Camera
from matrix import *
from funcs import get_scr_coords

class Object:
    def __init__(self, verticales: list=list(), edges: set=set()):
        self.m_model = Matrix(4, 4)
        self.verticales = verticales
        self.edges = edges
        self.tr = [0.0, 0.0, 0.0]
        self.r_x = 0
        self.r_y = 0
        self.r_z = 0
    def __repr__(self):
        return self.verticales.__repr__()
    def __iter__(self):
        return self.verticales.__iter__()
    def __getitem__(self, idx):
        return self.verticales[idx]
    def move(self, dx: int | float, dy: int | float, dz: int | float):
        self.tr[0] += float(dx)
        self.tr[1] += float(dy)
        self.tr[2] += float(dz)
    def rot_x(self, degrees: int):
        self.r_x = (self.r_x + degrees) % 360
    def rot_y(self, degrees: int):
        self.r_y = (self.r_y + degrees) % 360
    def rot_z(self, degrees: int):
        self.r_z = (self.r_z + degrees) % 360
    def update_matrix(self):
        self.m_model = M_tr(*self.tr) * M_rot_z(self.r_z) * M_rot_y(self.r_y) * M_rot_x(self.r_x)
    def render(self, surface: pg.Surface, cam: Camera):
        self.update_matrix()
        proj_vs = [get_scr_coords(cam.get_v_matrix() * self.m_model * v) for v in self.verticales]
        [pg.draw.line(surface, 'green', proj_vs[edge[0]], proj_vs[edge[1]], 1) for edge in self.edges]
        
class Cube(Object):
    def __init__(self, x0: int | float, y0: int | float, z0: int | float, a: int | float):
        
        h = a / 2.0  
        # front face
        v0 = Matrix(data=[x0 - h, y0 + h, z0 + h, 1])  # top left
        v1 = Matrix(data=[x0 + h, y0 + h, z0 + h, 1])  # top right
        v2 = Matrix(data=[x0 + h, y0 - h, z0 + h, 1])  # bottom right
        v3 = Matrix(data=[x0 - h, y0 - h, z0 + h, 1])  # bottom left
        # back face
        v4 = Matrix(data=[x0 - h, y0 + h, z0 - h, 1])  # top left
        v5 = Matrix(data=[x0 + h, y0 + h, z0 - h, 1])  # top right
        v6 = Matrix(data=[x0 + h, y0 - h, z0 - h, 1])  # bottom right
        v7 = Matrix(data=[x0 - h, y0 - h, z0 - h, 1])  # bottom left
        verticales = [v0, v1, v2, v3, v4, v5, v6, v7]
        edges = set([
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ])
        super().__init__(verticales, edges)
        
class Scene:
    def __init__(self, objects: list[Object] = list()):
        self.objects = objects
    def __repr__(self):
        return self.objects.__repr__()
    def __iter__(self):
        return self.objects.__iter__()
    def __getitem__(self, idx):
        return self.objects[idx]
    def append(self, obj: Object) -> None:
        self.objects.append(obj)
    def render(self, surface: pg.Surface, cam: Camera):
        [obj.render(surface, cam) for obj in self]
        

def load_obj(filepath: str) -> Object:
    vertices = []
    edges = set()
    all_x, all_y, all_z = [], [], []

    with open(filepath, 'r') as file:
        for line in file:
            tokens = line.strip().split()
            
            if not tokens:
                continue
            
            if tokens[0] == 'v':
                x = float(tokens[1])
                y = float(tokens[2])
                z = float(tokens[3])
                vertices.append([x, y, z])
                all_x.append(x)
                all_y.append(y)
                all_z.append(z)
            
            if tokens[0] == 'f':
                face_vertices  = [int(token.split('/')[0]) - 1 for token in tokens[1:]]
                num_vs = len(face_vertices)
                for i in range(num_vs):
                    v1 = face_vertices [i]
                    v2 = face_vertices [(i + 1) % num_vs]

                    edges.add((min(v1, v2), max(v1, v2)))
        
        center_x = (min(all_x) + max(all_x)) / 2.0
        center_y = (min(all_y) + max(all_y)) / 2.0
        center_z = (min(all_z) + max(all_z)) / 2.0
        
        final_vertices = [
            Matrix(data=[
            v[0] - center_x, 
            v[1] - center_y, 
            v[2] - center_z, 
            1.0
            ]) for v in vertices
        ]
            
    return Object(verticales=final_vertices, edges=list(edges))
