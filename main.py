import pygame as pg
#import thorpy
import time
import numpy as np
from color import color
import scene
import game_manager as gm
import game_core as gc

# import map          RENAME MODULE map.py


alive = True


def handle_events(events):
    global alive
    for event in events:
        if event.type == pg.QUIT:
            alive = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                alive = False
                print('Exited game')

            keys = pg.key.get_pressed()

        if event.type == pg.MOUSEBUTTONDOWN:
            gm.clickpos = pg.mouse.get_pos()
            gm.last_clicked_camera_pos = gm.camera_pos
            # print(gm.ScreenToScene(gm, gm.clickpos))


def main():
    pg.init()

    screen = pg.display.set_mode((gm.screen_width, gm.screen_height))
    for i in range(10):
        gc.born_cell([gm.scene_width * np.random.rand(), gm.scene_height * np.random.rand()], color.random())

    while alive:
        # pg.key.set_repeat(10, 10)
        handle_events(pg.event.get())

        keys_pressed = pg.key.get_pressed()

        if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
            gm.move_camera(gm, (-1, 0))
        if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
            gm.move_camera(gm, (+1, 0))
        if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
            gm.move_camera(gm, (0, +1))
        if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]:
            gm.move_camera(gm, (0, -1))

        if gm.frame % (gm.FPS // gm.Game_FPS) == 0:
            for cell in gc.cells:
                if gm.clickpos is not None:
                    move_to = gm.ScreenToScene(gm, gm.clickpos)
                    cell.move(move_to)
        scene.scene_display(screen, gm.camera_pos, [gm.screen_width, gm.screen_height], gm.zoom, color.WHITE)
        scene.draw_cells(screen, gc.cells, gm.camera_pos, [gm.screen_width, gm.screen_height], gm.zoom)


        pg.display.update()
        time.sleep(1.0 / gm.Game_FPS)
        gm.frame += 1


if __name__ == "__main__":
    main()
