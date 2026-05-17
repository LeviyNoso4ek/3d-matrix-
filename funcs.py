from matrix import *
from constants import WIDTH, HEIGHT

def get_scr_coords(world_vertex: Matrix):
    proj_vertex = M_PROJ * world_vertex
    w = proj_vertex[3][0]
    x_ind = proj_vertex[0][0] / w + 1
    y_ind = proj_vertex[1][0] / w + 1
    x = x_ind / 2 * WIDTH
    y = HEIGHT - (y_ind / 2 * HEIGHT)
    return (int(x), int(y))

