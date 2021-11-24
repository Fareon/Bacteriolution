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


# подсказка для вызова scene_display()
'''
pg.init() # просто делаем экранчик
width = 400
height = 600
screen = pg.display.set_mode((width, height))


class Drawble_bjects():  # класс отрисовываемых объектов (тут можно подсмотреть необходимые атрибуты)
    def __init__(self, x, y, r, color=[]):
        self.x = x
        self.y = y
        self.color = color
        self.r = r


obj1 = Drawble_bjects(20, 25, 2, (0, 0, 0))  # создаём экземпляры и формируем список из них
obj2 = Drawble_bjects(0, 40, 4, (56, 153, 203))
objects = []
objects.append(obj1)
objects.append(obj2)

#-------------вызов функции---------------
scene_display(screen, objects, [20, 25], [width, height], 10, (255, 255, 255))
# screen
# objects - массив с экземплярами класса, имеющего атрибуты .x .y .r .color
# [20, 25] - коордиаты камеры, не обязательно целые
# [width, height] - размеры поля для рисования
# 10 - zoom (размер одного пикселя (в экранных пикселях))
# (255, 255, 255) - цвет фона

# scene_display(screen, objects, [camera_x_cord, camera_y_cord], [screen_width, screen_height], zoom, background_color)
'''

if __name__ == "__main__":
    main()