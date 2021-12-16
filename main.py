import pygame as pg
import pygame_gui
import ui
import time
import color
import scene
import sound
import game_manager as gm
import game_core as gc
import tricky_functions as f

alive = True
playing = True


def handle_events(events):
    """
    This function stands for processing events
    :param events: events the function has to process
    """
    # Calling for all the global names
    global alive
    global playing

    for event in events:
        if event.type == pg.USEREVENT:
            # Checking if "mutate" button is pressed
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == ui.mutate_button:
                    new_color = color.random_color()

                    # Actual mutating
                    for cell in gc.self_cells:
                        cell.player_mutate(new_color)
                        ui.change_cell_icon_color(cell.color)
                        ui.cell_icon_button.rebuild_from_changed_theme_data()

                if event.ui_element == ui.info_panel_button:
                    gm.ui_click = True

    for event in events:
        ui.manager.process_events(event)

        # Checking if we need to escape
        if event.type == pg.QUIT:
            alive = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sound.shut_down_music()
                alive = False
            '''if event.key == pg.K_x:
                print('cells:', len(gc.cells))
                print('Self_cells:', len(gc.self_cells))
                gc.debug_grid()'''

            keys = pg.key.get_pressed()

        if event.type == pg.MOUSEBUTTONDOWN:

            # If the game is not going not, it start after clicking
            if not playing:
                playing = True
                gc.generate_level(food_gens=9, cells=5, self_cells=1)

            if pg.mouse.get_pos()[0] > gm.ui_panel_width:
                gm.clickpos = pg.mouse.get_pos()
                gm.last_clicked_camera_pos = gm.camera_pos
            if event.button == 4:
                gm.do_zoom(gm, +1)
            if event.button == 5:
                gm.do_zoom(gm, -1)

    gm.ui_click = False


def check_win_condition(screen, screen_size=None):
    """
    This function checks if the game is won or lost, and shows screens of defeat and victory
    :param screen: pygame screen
    :param screen_size: size of the screen
    """
    global playing

    if screen_size is None:
        screen_size = [gm.screen_width, gm.screen_height]

    # Losing condition
    if len(gc.self_cells) == 0:
        scene.show_defeat_screen(screen, screen_size)
        playing = False

    # Winning condition
    if len(gc.cells) == 0:
        scene.show_victory_screen(screen, screen_size)
        playing = False


def main():
    """
    Initializes main cycle of the game
    """
    pg.init()

    pg.display.set_caption('Bacteriolution')
    pg.font.init()

    screen = pg.display.set_mode((gm.screen_width, gm.screen_height))

    gc.generate_level(food_gens=9, cells=5, self_cells=1)

    while alive:
        handle_events(pg.event.get())

        if ui.game_speed_scrbar.check_has_moved_recently():
            gm.Game_FPS = 50 + ui.game_speed_scrbar.scroll_position / 98 * 65  # bad code
            print(ui.game_speed_scrbar.scroll_position)

        # DETECT INPUT
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

        # must go through all events here additionaly, otherwise won't scroll continuesly

        # CALCULATE NEW POS
        if gm.frame % (gm.FPS // gm.Game_FPS) == 0 and playing:
            # any gamecore events happen here
            for cell in gc.self_cells:
                gc.eat_food(cell, gc.self_cells)
                if gm.clickpos is not None:
                    move_to = gm.ScreenToScene(gm, gm.clickpos)
                    cell.move(move_to, gc.grid)
            for cell in gc.cells:
                gc.eat_food(cell, gc.cells)
                cell.move(cell.think_ahead(gc.cells + gc.self_cells, gc.food_generators, gc.food), gc.grid)

            for food_gen in gc.food_generators:
                if f.chance(food_gen.rate):
                    food_gen.gen_food(gm.scene_width, gm.scene_height, gc.grid, gc.food)

        # GRAPHICS
        scene.draw_background(screen, color.WHITE)

        scene.draw_sqare_objects(screen, gc.food, gm.camera_pos, [gm.screen_width, gm.screen_height],
                                 gm.zoom)  # draw food
        scene.draw_sqare_objects(screen, gc.cells + gc.self_cells, gm.camera_pos, [gm.screen_width, gm.screen_height],
                                 gm.zoom)  # draw cells
        scene.draw_borders(screen, [gm.screen_width, gm.screen_height], gm.zoom,
                           [gm.scene_width, gm.scene_height], color.random_color(), gm.borders_width, gm.camera_pos)
        scene.draw_cross_objects(screen, gc.food_generators, gm.camera_pos, [gm.screen_width, gm.screen_height],
                                 gm.zoom)  # draw foodgens

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


        ui.draw_text(screen)
        # scene.show_defeat_screen(screen, [gm.screen_width, gm.screen_height] )
        check_win_condition(screen, screen_size=[gm.screen_width, gm.screen_height])

        pg.display.update()
        time.sleep(1.0 / gm.Game_FPS)
        gm.frame += 1


if __name__ == "__main__":
    sound.play_background_music()
    main()
