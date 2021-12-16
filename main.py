import pygame
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
        if event.type == pygame.USEREVENT:
            # Checking if "Mutate" button is pressed
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
        if event.type == pygame.QUIT:
            alive = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sound.shut_down_music()
                alive = False
            '''if event.key == pg.K_x:
                print('cells:', len(gc.cells))
                print('Self_cells:', len(gc.self_cells))
                gc.debug_grid()'''

        if event.type == pygame.MOUSEBUTTONDOWN:

            # If the game is not going not, it start after clicking
            if not playing:
                playing = True

                gc.generate_level(food_gens=9, cells=5, self_cells=1)

            if pygame.mouse.get_pos()[0] > gm.ui_panel_width:
                gm.click_pos = pygame.mouse.get_pos()
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
        ui.change_cell_icon_color(color.INIT_PLAYER_COLOR)
        playing = False

    # Winning condition
    elif len(gc.cells) == 0:
        scene.show_victory_screen(screen, screen_size)
        ui.change_cell_icon_color(color.INIT_PLAYER_COLOR)
        playing = False


def main():
    """
    Initializes main cycle of the game
    """
    pygame.init()

    pygame.display.set_caption('Bacteriolution')
    pygame.font.init()

    screen = pygame.display.set_mode((gm.screen_width, gm.screen_height))

    gc.generate_level(food_gens=9, cells=5, self_cells=1)

    while alive:
        handle_events(pygame.event.get())

        if ui.game_speed_scroll_bar.check_has_moved_recently():
            gm.Game_FPS = 60 + ui.game_speed_scroll_bar.scroll_position / 2

        # Detecting input
        keys_pressed = pygame.key.get_pressed()

        # Giving response (moving camera)
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            gm.move_camera(gm, (-1, 0))
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            gm.move_camera(gm, (+1, 0))
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            gm.move_camera(gm, (0, +1))
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            gm.move_camera(gm, (0, -1))

        # Giving response (zooming)
        if keys_pressed[pygame.K_z]:
            gm.do_zoom(gm, +1)
        if keys_pressed[pygame.K_x]:
            gm.do_zoom(gm, -1)

        # We must go through all events here additionally, otherwise won't scroll continuously

        # Calculating new position
        if gm.frame % (gm.FPS // gm.Game_FPS) == 0 and playing:

            # Any game core events happen here
            for cell in gc.self_cells:
                gc.eat_food(cell, gc.self_cells)
                if gm.click_pos is not None:
                    move_to = gm.screen_to_scene(gm, gm.click_pos)
                    cell.move(move_to, gc.grid)

            for cell in gc.cells:
                gc.eat_food(cell, gc.cells)
                cell.move(cell.think_ahead(gc.cells + gc.self_cells, gc.food_generators, gc.food), gc.grid)

            for food_gen in gc.food_generators:
                if f.chance(food_gen.rate):
                    food_gen.gen_food(gm.scene_width, gm.scene_height, gc.grid, gc.food)

        # Graphics
        # Updating background
        scene.draw_background(screen, color.WHITE)

        # Drawing food
        scene.draw_square_objects(screen, gc.food, gm.camera_pos, [gm.screen_width, gm.screen_height], gm.zoom)
        # Drawing cells
        scene.draw_square_objects(
            screen,
            gc.cells + gc.self_cells,
            gm.camera_pos,
            [gm.screen_width, gm.screen_height],
            gm.zoom
        )
        # Drawing borders
        scene.draw_borders(
            screen,
            [gm.screen_width, gm.screen_height],
            gm.zoom,
            [gm.scene_width, gm.scene_height],
            color.random_color(),
            gm.borders_width,
            gm.camera_pos
        )
        # Drawing food generators
        scene.draw_cross_objects(
            screen,
            gc.food_generators,
            gm.camera_pos,
            [gm.screen_width, gm.screen_height],
            gm.zoom
        )

        ui.manager.update(1.0 / gm.Game_FPS)
        ui.manager.draw_ui(screen)
        ui.draw_text(screen)

        check_win_condition(screen, screen_size=[gm.screen_width, gm.screen_height])

        pygame.display.update()
        time.sleep(1.0 / gm.Game_FPS)
        gm.frame += 1


# Beginning the game
if __name__ == "__main__":
    sound.play_background_music()
    main()
