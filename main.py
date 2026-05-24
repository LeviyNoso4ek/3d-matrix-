from camera import Camera
from matrix import *
from objects import *
from constants import *
from vec import Vec3
import pygame as pg

root = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('chel-v-matrice')

cam = Camera(Vec3(0, 0, 0))

scene = Scene()
obj = load_obj('models/cat.obj')
scene.append(obj)
obj.move(0, 0, 4)

running = True
clock = pg.time.Clock()
while running:
    root.fill('black')

    for e in pg.event.get():
        if e.type == pg.MOUSEBUTTONDOWN:
            pass
        if e.type == pg.QUIT:
            running = False
            
    obj.rot_y(1)

    scene.render(root, cam)
    pg.display.flip()
    clock.tick(60)
pg.quit()