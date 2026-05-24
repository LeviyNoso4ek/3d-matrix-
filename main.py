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
playing = True

clock = pg.time.Clock()

pg.mouse.set_visible(not playing)

while running:
    root.fill('black')

    for e in pg.event.get():
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                playing = not playing
                pg.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
                pg.mouse.get_rel()
                pg.mouse.set_visible(not playing)

        if e.type == pg.QUIT:
            running = False
            
    keys = pg.key.get_pressed()
    move_speed = 0.1

    if keys[pg.K_w]:
        cam.P -= Vec3(cam.F.dot(Vec3(1, 0, 0)), 0, cam.F.dot(Vec3(0, 0, 1))).norm() * move_speed
    if keys[pg.K_s]:
        cam.P += Vec3(cam.F.dot(Vec3(1, 0, 0)), 0, cam.F.dot(Vec3(0, 0, 1))).norm() * move_speed
    if keys[pg.K_a]:
        cam.P -= Vec3(cam.R.dot(Vec3(1, 0, 0)), 0, cam.R.dot(Vec3(0, 0, 1))).norm() * move_speed
    if keys[pg.K_d]:
        cam.P += Vec3(cam.R.dot(Vec3(1, 0, 0)), 0, cam.R.dot(Vec3(0, 0, 1))).norm() * move_speed
    if keys[pg.K_SPACE]:
        cam.P += cam.world_up * move_speed
    if keys[pg.K_LSHIFT]:
        cam.P -= cam.world_up * move_speed
        
    if playing:
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        pg.mouse.set_pos((WIDTH // 2, HEIGHT // 2))

        if mouse_dx != 0 or mouse_dy != 0:
            cam.rot(-mouse_dx * SENSITIVITY, mouse_dy * SENSITIVITY)
            
    obj.rot_y(1)

    scene.render(root, cam)
    pg.display.flip()
    clock.tick(60)
pg.quit()