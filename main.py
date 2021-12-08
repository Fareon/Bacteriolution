import pygame as pg
import pygame_gui
import ui
#import thorpy
import time
import numpy as np
from color import color
import scene
import game_manager as gm
import game_core as gc
from random import randint
import tricky_functions as f

# import map          RENAME MODULE map.py


alive = True


def handle_events(events):
    global alive
    for event in events:
        
        if event.type == pg.USEREVENT:
             if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                 if event.ui_element == ui.info_panel_button:
                     gm.ui_click = True
                     print('Iteracted with ui')
                     
                     
        
        ui.manager.process_events(event)
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
            if(event.button == 4):
                gm.do_zoom(gm, +1)
            if (event.button == 5):
                gm.do_zoom(gm, -1)
                
        gm.ui_click = False


def main():
    pg.init()
    
    pg.display.set_caption('Bacteriolution')

    screen = pg.display.set_mode((gm.screen_width, gm.screen_height))
    borders_width = 2 #map visual borders

    for i in range(7):
        x_born = randint(3*borders_width, gm.scene_width - 3*borders_width)
        y_born = randint(3*borders_width, gm.scene_height - 3*borders_width)
        gc.born_food_gen((x_born, y_born))

    for i in range(1, 25):
        x_born = randint(3*borders_width, gm.scene_width - 3*borders_width)
        y_born = randint(3*borders_width, gm.scene_height - 3*borders_width)
        gc.born_cell([x_born, y_born], color.random(), i)

    for i in range(2):
        x_born = randint(3*borders_width, gm.scene_width - 3*borders_width)
        y_born = randint(3*borders_width, gm.scene_height - 3*borders_width)
        gc.born_self_cell([x_born, y_born], color.random(), i)

    while alive:
        handle_events(pg.event.get())

        #DETECT INPUT
        keys_pressed = pg.key.get_pressed()

        if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
            gm.move_camera(gm, (-1, 0))
        if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
            gm.move_camera(gm, (+1, 0))
        if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
            gm.move_camera(gm, (0, +1))
        if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]:
            gm.move_camera(gm, (0, -1))

        if keys_pressed[pg.K_z]:
            gm.do_zoom(gm, +1)
        if keys_pressed[pg.K_x]:
            gm.do_zoom(gm, -1)

        #must go through all events here additionaly, otherwise won't scroll continuesly


        # CALCULATE NEW POS
        if gm.frame % (gm.FPS // gm.Game_FPS) == 0:
            #any gamecore events happen here
            for cell in gc.self_cells:
                if gm.clickpos is not None:
                    move_to = gm.ScreenToScene(gm, gm.clickpos)
                    cell.move(move_to)
                gc.eat_food(cell)
            for cell in gc.cells:
                cell.move(cell.think_ahead(gc.cells+gc.self_cells, gc.food_generators, gc.food))
                gc.eat_food(cell)

            for food_gen in gc.food_generators:
                if f.chance(food_gen.rate):
                    food_gen.gen_food()

        # GRAPHICS
        scene.draw_background(screen, color.WHITE)

        scene.draw_sqare_objects(screen, gc.food, gm.camera_pos, [gm.screen_width, gm.screen_height],
                                 gm.zoom)  # draw food
        scene.draw_sqare_objects(screen, gc.cells+gc.self_cells, gm.camera_pos, [gm.screen_width, gm.screen_height], gm.zoom) #draw cells
        scene.draw_borders(screen, [gm.screen_width, gm.screen_height], gm.zoom,
                     [gm.scene_width, gm.scene_height], color.random(), borders_width, gm.camera_pos)
        scene.draw_cross_objects(screen, gc.food_generators, gm.camera_pos, [gm.screen_width, gm.screen_height], gm.zoom) #draw foodgens

        # еду рисуем при помощи той же функции, что и клетки

        # источники еды рисуем с помощью функции draw_cross_objects(), входные данные такие же как у draw_sqare_objects()
        # только отрисовывается крест, вписанный в соответствующий квадрат

        # отрисовка границ:
        # draw_borders(screen, [gm.screen_width, gm.screen_height], gm.zoom,
        # gamefield_size, borders_color, borders_width, gm.camera_pos)

        # gamefield_size = [gamefield_width, gamefield_height] - размеры игрового поля, где может находиться клетка
        # borders_width - толщина границы в наших пикселях

        
        ui.manager.update(1.0 / gm.Game_FPS)
        ui.manager.draw_ui(screen)
        
        pg.display.update()
        time.sleep(1.0 / gm.Game_FPS)
        gm.frame += 1


if __name__ == "__main__":
    main()
