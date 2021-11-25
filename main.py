import pygame as pg
import thorpy
import time
import numpy as np
from color import color
import play_units, scene 
#import map          RENAME MODULE map.py


alive = True

def handle_events(events):
    global alive
    for event in events:
        if event.type == pg.QUIT:
            alive = False

def main():
    pg.init()
    
    width = 1280
    height = 650
    FPS = 20
    
    #INITIAL SHIT
    cells = [play_units.Cell(+50, -50, color.random()) ]
            
    screen = pg.display.set_mode((width, height))
    #drawer = solar_vis.Drawer(screen)
    #menu, box, timer = init_ui(screen)

    while alive:
        handle_events(pg.event.get())
        
        for cell in cells:
            cell.move((0, 0))
        scene.scene_display(screen, cells, [0, 0], [width, height], 10, color.WHITE)
        
        
        time.sleep(1.0 / FPS)


# подсказка для вызова scene_display()

class Drawble_bjects():  # класс отрисовываемых объектов (тут можно подсмотреть необходимые атрибуты)
    def __init__(self, x, y, r, color=[]):
        self.x = x
        self.y = y
        self.color = color
        self.r = r



if __name__ == "__main__":
    main()