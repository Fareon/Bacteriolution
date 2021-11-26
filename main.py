import pygame as pg
import thorpy
import time
import numpy as np


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
    FPS = 60
    
    screen = pg.display.set_mode((width, height))
    #drawer = solar_vis.Drawer(screen)
    #menu, box, timer = init_ui(screen)

    while alive:
        handle_events(pg.event.get())
        time.sleep(1.0 / FPS)


if __name__ == "__main__":
    main()