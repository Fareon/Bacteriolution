import pygame as pg


def draw_background(screen, background_color):
    '''
    draw background
    :param screen:
    :param background_color:
    '''
    screen.fill(background_color)


def draw_borders(screen, screen_size, zoom, gamefield_size, borders_color, borders_width, camera_pos):
    '''
    function that draw borders
    :param screen:
    :param screen_size:  [screen_with, screen_height]
    :param zoom: how much bigger should be our pixel (element of our pixel set), then screen pixel
    :param gamefield_size: [gamefield_with, gamefield_height]
    :param borders_color:
    :param borders_width: int. with of border in pixels
    :param camera_pos: coords of camera [x, y]
    '''
    if zoom < 1: # if zoom < 1 border can't be drawn
        zoom =1
    pixel_size = zoom
    pixel_view_amount = [int(screen_size[0] / zoom) + 1, int(screen_size[1] / zoom) + 1]
    # coords of up left frame-border corner in new system of coords
    x0 = -camera_pos[0] + int((pixel_view_amount[0]) / 2) - borders_width
    y0 = -camera_pos[1] + int((pixel_view_amount[1]) / 2) - borders_width
    # draw up border
    pg.draw.rect(screen, borders_color,
                 (x0 * pixel_size, y0 * pixel_size,
                  (gamefield_size[0] + 2 * borders_width) * pixel_size, borders_width * pixel_size))
    # draw left border
    pg.draw.rect(screen, borders_color,
                 (x0 * pixel_size, y0 * pixel_size,
                  borders_width * pixel_size, (gamefield_size[1] + 2 * borders_width) * pixel_size))
    # draw down border
    pg.draw.rect(screen, borders_color,
                 (x0 * pixel_size, (y0 + gamefield_size[1] + borders_width) * pixel_size,
                  (gamefield_size[0] + 2 * borders_width) * pixel_size, borders_width * pixel_size))
    # draw right border
    pg.draw.rect(screen, borders_color,
                 ((x0 + gamefield_size[0] + borders_width) * pixel_size, y0 * pixel_size,
                  borders_width * pixel_size, (gamefield_size[1] + 2 * borders_width) * pixel_size))


def choose_objects_for_drawing(objects, camera_pos, pixel_view_amount):
    '''
    we check if object from array objects situated on our screen and should be drawn
    :param objects: list with objects we want to draw
    :param camera_pos: coords of camera [x, y]
    :param pixel_view_amount: how many pixels we want to draw [row length, column length]
    '''
    int_camera_coords = [int(camera_pos[0]), int(camera_pos[1])]
    scene_objects = []  # list of objects, located in camera area
    for obj in objects:
        x = obj.x - int_camera_coords[0]
        y = -1 * (obj.y - int_camera_coords[1])
        r = obj.r
        if ((abs(x) <= (pixel_view_amount[0] + 1) / 2 + r) and (abs(y) <= (pixel_view_amount[1] + 1) / 2 + r)):
            scene_objects.append(
                [int(x + (pixel_view_amount[0]) / 2), int(y + (pixel_view_amount[1]) / 2), r, obj.color])
            # there are objects in new system of coords in this list
    return scene_objects


def sqare_objects_display(screen, pixel_size, scene_objects):
    '''
    display square shaped objects
    :param screen:
    :param pixel_size: size of net in our coords system
    :param scene_objects: # list of objects, located in camera area
    '''
    for obj in scene_objects:
        x = obj[0]
        y = obj[1]
        r = obj[2]
        color = obj[3]
        pg.draw.rect(screen, color,
                     ((x - r) * pixel_size, (y - r) * pixel_size, 2 * r * pixel_size, 2 * r * pixel_size))


def cross_objects_display(screen, pixel_size, scene_objects):
    '''
    display cross shaped objects
    :param screen:
    :param pixel_size: size of net in our coords system
    :param scene_objects: # list of objects, located in camera area
    '''
    for obj in scene_objects:
        x = obj[0]
        y = obj[1]
        r = obj[2]
        color = obj[3]
        pg.draw.rect(screen, color,
                     ((x - r / 2) * pixel_size, (y - r) * pixel_size, r * pixel_size, 2 * r * pixel_size))
        pg.draw.rect(screen, color,
                     ((x - r) * pixel_size, (y - r / 2) * pixel_size, 2 * r * pixel_size, r * pixel_size))


def scene_display(screen, camera_pos, screen_size, background_color):
    '''
    function that display scene (without objects)
    :param screen:
    :param camera_pos: coords of camera [x, y]
    :param screen_size: [screen_with, screen_height]
    :param zoom: How much bigger should be our pixel (element of our pixel set), then screen pixel
    :param background_color:
    '''
    draw_background(screen, background_color)


def draw_sqare_objects(screen, objects, camera_pos, screen_size, zoom):
    '''
    function that display objects which have square shape
    :param screen:
    :param objects: list with objects we want to draw (need obj.r .x .y .color)
    :param camera_pos: coords of camera [x, y]
    :param screen_size: [screen_with, screen_height]
    :param zoom: How much bigger should be our pixel (element of our pixel set), then screen pixel
    '''
    dx = camera_pos[0] - int(camera_pos[0])  # offset of pixel net, related not int coords of camera
    dy = camera_pos[1] - int(camera_pos[1])
    pixel_size = zoom
    pixel_view_amount = [int(screen_size[0] / zoom) + 1, int(screen_size[1] / zoom) + 1]
    scene_cells = choose_objects_for_drawing(objects, camera_pos, pixel_view_amount)
    sqare_objects_display(screen, pixel_size, scene_cells)


def draw_cross_objects(screen, objects, camera_pos, screen_size, zoom):
    '''
    function that display objects which have square shape
    :param screen:
    :param objects: list with objects we want to draw (need obj.r .x .y .color)
    :param camera_pos: coords of camera [x, y]
    :param screen_size: [screen_with, screen_height]
    :param zoom: How much bigger should be our pixel (element of our pixel set), then screen pixel
    '''
    dx = camera_pos[0] - int(camera_pos[0])  # offset of pixel net, related not int coords of camera
    dy = camera_pos[1] - int(camera_pos[1])
    pixel_size = zoom
    pixel_view_amount = [int(screen_size[0] / zoom) + 1, int(screen_size[1] / zoom) + 1]
    scene_cells = choose_objects_for_drawing(objects, camera_pos, pixel_view_amount)
    cross_objects_display(screen, pixel_size, scene_cells)
