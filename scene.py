import pygame

square_outline_color = (57, 57, 57)
square_outline_width = 1


def draw_background(screen, background_color):
    """
    Draws background
    :param screen: pygame screen
    :param background_color: color of the back ground
    """
    screen.fill(background_color)


def draw_borders(screen, screen_size, zoom, game_field_size, borders_color, borders_width, camera_pos):
    """
    Function that draws borders
    :param screen: pygame screen
    :param screen_size:  [screen_with, screen_height]
    :param zoom: how much bigger should be our pixel (element of our pixel set), then screen pixel
    :param game_field_size: [game_field_with, game_field_height]
    :param borders_color:
    :param borders_width: int. with of border in pixels
    :param camera_pos: coordinates of camera [x, y]
    """
    pixel_size = zoom

    # Coordinates of the top-left frame-border corner in new system of coordinates
    x0 = -camera_pos[0] + screen_size[0] / (2 * zoom) - borders_width
    y0 = camera_pos[1] + screen_size[1] / (2 * zoom) - borders_width - game_field_size[1]

    borders_width_in_real_pixels = borders_width * pixel_size

    if borders_width_in_real_pixels < 1:
        borders_width_in_real_pixels = 1
    # Drawing top border
    pygame.draw.rect(
        screen,
        borders_color,
        (x0 * pixel_size,
         y0 * pixel_size,
         (game_field_size[0] + 2 * borders_width) * pixel_size,
         borders_width_in_real_pixels)
    )
    # Drawing left border
    pygame.draw.rect(
        screen,
        borders_color,
        (x0 * pixel_size,
         y0 * pixel_size,
         borders_width_in_real_pixels,
         (game_field_size[1] + 2 * borders_width) * pixel_size
         )
    )
    # Drawing bottom border
    pygame.draw.rect(
        screen,
        borders_color,
        (x0 * pixel_size,
         (y0 + game_field_size[1] + 1 * borders_width) * pixel_size,
         (game_field_size[0] + 2 * borders_width) * pixel_size,
         borders_width_in_real_pixels
         )
    )
    # Drawing right border
    pygame.draw.rect(
        screen,
        borders_color,
        ((x0 + game_field_size[0] + borders_width) * pixel_size,
         y0 * pixel_size,
         borders_width_in_real_pixels,
         (game_field_size[1] + 2 * borders_width) * pixel_size
         )
    )


def choose_objects_for_drawing(objects, camera_pos, screen_size, zoom):
    """
    Checks whether an object from the array objects situated on our screen and should be drawn
    :param objects: list with objects we want to draw
    :param camera_pos: coordinates of camera [x, y]
    :param screen_size: [screen_with, screen_height]
    :param zoom: how much bigger should be our pixel (element of our pixel set), then screen pixel
    """
    # How many pixels we want to draw [row length, column length]
    pixel_view_amount = [int(screen_size[0] / zoom) + 1, int(screen_size[1] / zoom) + 1]

    scene_objects = []  # list of objects, located in camera area

    for obj in objects:
        x = obj.x - camera_pos[0]
        y = -1 * (obj.y - camera_pos[1])
        r = obj.r
        if (abs(x) <= pixel_view_amount[0] / 2 + r) and (abs(y) <= pixel_view_amount[1] / 2 + r):
            scene_objects.append(
                [x + screen_size[0] / (2 * zoom),
                 y + screen_size[1] / (2 * zoom),
                 r,
                 obj.color]
            )

    # Now there are objects in new system of coordinates in this list
    return scene_objects


def square_objects_display(screen, pixel_size, scene_objects):
    """
    Display square shaped objects
    :param screen: pygame screen
    :param pixel_size: size of net in our coordinates system
    :param scene_objects: list of objects, located in camera area
    """
    for obj in scene_objects:
        x = obj[0]
        y = obj[1]
        r = obj[2]
        color = obj[3]
        pygame.draw.rect(
            screen,
            color,
            ((x - r) * pixel_size, (y - r) * pixel_size, 2 * r * pixel_size, 2 * r * pixel_size)
        )
        pygame.draw.rect(
            screen,
            square_outline_color,
            ((x - r) * pixel_size, (y - r) * pixel_size, 2 * r * pixel_size, 2 * r * pixel_size),
            square_outline_width
        )


def cross_objects_display(screen, pixel_size, scene_objects):
    """
    Display cross shaped objects
    :param screen: pygame screen
    :param pixel_size: size of net in our coordinates system
    :param scene_objects: list of objects, located in camera area
    """
    for obj in scene_objects:
        x = obj[0]
        y = obj[1]
        r = obj[2]
        color = obj[3]
        pygame.draw.rect(
            screen,
            color,
            ((x - r / 2) * pixel_size, (y - r) * pixel_size, r * pixel_size, 2 * r * pixel_size)
        )
        pygame.draw.rect(
            screen,
            color,
            ((x - r) * pixel_size, (y - r / 2) * pixel_size, 2 * r * pixel_size, r * pixel_size)
        )


def draw_square_objects(screen, objects, camera_pos, screen_size, zoom):
    """
    Function that display objects which have square shape
    :param screen: pygame screen
    :param objects: list with objects we want to draw (need obj.r .x .y .color)
    :param camera_pos: coordinates of camera [x, y]
    :param screen_size: [screen_with, screen_height]
    :param zoom: how much bigger should be our pixel (element of our pixel set), then screen pixel
    """
    pixel_size = zoom
    scene_cells = choose_objects_for_drawing(objects, camera_pos, screen_size, zoom)
    square_objects_display(screen, pixel_size, scene_cells)


def draw_cross_objects(screen, objects, camera_pos, screen_size, zoom):
    """
    Function that display objects which have square shape
    :param screen: pygame screen
    :param objects: list with objects we want to draw (need obj.r .x .y .color)
    :param camera_pos: coordinates of camera [x, y]
    :param screen_size: [screen_with, screen_height]
    :param zoom: How much bigger should be our pixel (element of our pixel set), then screen pixel
    """
    pixel_size = zoom
    scene_cells = choose_objects_for_drawing(objects, camera_pos, screen_size, zoom)
    cross_objects_display(screen, pixel_size, scene_cells)


def show_defeat_screen(screen, screen_size):
    """
    Function, that shows defeat screen
    :param screen: pygame screen
    :param screen_size: [screen_with, screen_height]
    """
    surface = pygame.Surface((screen_size[0], screen_size[1]), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 220), (0, 0, screen_size[0], screen_size[1]))

    font = pygame.font.Font("Font/HyperStiffRoundBootiedOpossumRegular.ttf", 70)

    text = font.render("DEFEAT", False, (255, 0, 0))

    pos = text.get_rect(center=(screen_size[0] / 2, screen_size[1] / 2))

    screen.blit(surface, (0, 0))
    screen.blit(text, pos)


def show_victory_screen(screen, screen_size):
    """
    Function, that shows victory screen
    :param screen: pygame screen
    :param screen_size: [screen_with, screen_height]
    """
    surface = pygame.Surface((screen_size[0], screen_size[1]), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 220), (0, 0, screen_size[0], screen_size[1]))
    font = pygame.font.Font("Font/HyperStiffRoundBootiedOpossumRegular.ttf", 70)
    text = font.render("VICTORY", 0, (0, 255, 0))
    pos = text.get_rect(center=(screen_size[0] / 2, screen_size[1] / 2))
    screen.blit(surface, (0, 0))
    screen.blit(text, pos)
