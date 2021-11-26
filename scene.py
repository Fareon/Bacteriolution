import pygame as pg

def draw_background(screen, background_color, screen_size):
    '''
    draw background
    :param screen:
    :param background_color:
    :param screen_size: screen_size = [width, height]
    '''
    pg.draw.rect(screen, background_color,
                 (0, 0, screen_size[0], screen_size[1]))


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


def scene_objects_display(screen, pixel_size, scene_objects):
    '''
    draw scene_objects
    :param screen:
    :param scene_objects: # list of objects, located in camera area
    '''
    for obj in scene_objects:
        x = obj[0]
        y = obj[1]
        r = obj[2]
        color = obj[3]
        pg.draw.rect(screen, color,
                     ((x - r) * pixel_size, (y - r) * pixel_size, 2 * r * pixel_size, 2 * r * pixel_size))


def scene_display(screen, objects, camera_pos, screen_size, zoom, background_color):
    '''
    main function that display scene
    :param screen:
    :param objects: list with objects we want to draw (need obj.r .x .y .color)
    :param camera_pos: coords of camera [x, y]
    :param screen_size: [screen_with, screen_height]
    :param zoom: How much bigger should be our pixel (element of our pixel set), then screen pixel
    :param background_color:
    '''
    dx = camera_pos[0] - int(camera_pos[0])  # offset of pixel net, related not int coords of camera
    dy = camera_pos[1] - int(camera_pos[1])
    pixel_size = zoom
    pixel_view_amount = [int(screen_size[0] / zoom) + 1, int(screen_size[1] / zoom) + 1]
    scene_objects = choose_objects_for_drawing(objects, camera_pos, pixel_view_amount)
    draw_background(screen, background_color, screen_size)
    scene_objects_display(screen, pixel_size, scene_objects)
