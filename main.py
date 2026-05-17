from camera import Camera
from matrix import *
from objects import *
from constants import *
from vec import Vec3
import pygame as pg

root = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('3d')

scene = Scene()
skull = load_obj('man.obj')
scene.append(skull)
skull.move(0, 0, 10)
# skull.rot_x(90)
# skull.rot_z(180)
# skull.rot_y(30)
skull.update_matrix()

# cube1 = Cube(0, 0, 0, 1)
# scene.append(cube1)
# cube1.move(1, 2, 5.0)
# cube1.update_matrix()

# cube2 = Cube(0, 0, 0, 1)
# scene.append(cube2)
# cube2.move(-1, 2, 4.0)
# cube2.update_matrix()

running = True
clock = pg.time.Clock()
while running:
    root.fill('black')

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
    
    skull.rot_y(10)
    skull.rot_z(10)
    skull.update_matrix()

    scene.render(root)
    pg.display.flip()
    clock.tick(60)
pg.quit()