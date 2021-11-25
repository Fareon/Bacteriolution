import pygame as pg
import thorpy
import time
import numpy as np
from color import color
import play_units, scene
import game_manager as gm
#import map          RENAME MODULE map.py


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
        if event.type == pg.MOUSEBUTTONDOWN:
            gm.clickpos = pg.mouse.get_pos()
            print(gm.ScreenToScene(gm.clickpos))

def main():
    pg.init()
    
    #INITIAL SHIT
    cells = [play_units.Cell(+0, -0, color.random()) ]
            
    screen = pg.display.set_mode((gm.width, gm.height))
    #drawer = solar_vis.Drawer(screen)
    #menu, box, timer = init_ui(screen)

    while alive:
        handle_events(pg.event.get())
        
        for cell in cells:
            if(gm.clickpos != None):
                move_to = gm.ScreenToScene(gm.clickpos)
                cell.move(move_to)
        scene.scene_display(screen, cells, gm.camera_pos, [gm.width, gm.height], gm.zoom, color.WHITE)

        pg.display.update()
        time.sleep(1.0 / gm.FPS)

if __name__ == "__main__":
    main()