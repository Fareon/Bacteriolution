def draw_background(screen, background_color, screen_size):
    '''
    draw background
    :param screen:
    :param background_color:
    :param screen_size: screen_size = [width, height]
    '''
    pg.draw.rect(screen, background_color,
                 (0, 0, screen_size[0], screen_size[1]))


def pixel_colorise(objects, camera_pos, pixel_view_amount):
    '''
    we chose color for pixels, that we want to draw (pixels in camera area)
    :param objects: list with objects we want to draw
    :param camera_pos: coords of camera [x, y]
    :param pixel_view_amount: how many pixels we want to draw [row length, column length]
    :return pixels: 2 dimensional array with colors of pixels, we need to draw
    '''
    int_camera_coords = [int(camera_pos[0]), int(camera_pos[1])]
    scene_objects = []  # list of objects, located in camera area
    for obj in objects:
        x = obj.x - int_camera_coords[0]
        y = obj.y - int_camera_coords[1]
        r = obj.r
        if ((abs(x) <= (pixel_view_amount[0] + 1) / 2 + r) and (abs(y) <= (pixel_view_amount[1] + 1) / 2 + r)):
            scene_objects.append(
                [int(x + (pixel_view_amount[0]) / 2), int(y + (pixel_view_amount[1]) / 2), r, obj.color])
            # there are objects in new system of coords in this list
    pixels = [[0 for i in range(pixel_view_amount[1] + 1)]
              for j in range(pixel_view_amount[0] + 1)]  # creating list of pixels
    for obj in scene_objects:  # finally colorise pixels included in objects
        obj_x = obj[0]
        obj_y = obj[1]
        obj_r = obj[2]
        obj_color = obj[3]
        for x in range(-1 * obj_r, obj_r):
            for y in range(-1 * obj_r, obj_r):
                if ((obj_x + x >= 0) and (obj_x + x <= pixel_view_amount[0]) and
                        (obj_y + y >= 0) and (obj_y + y <= pixel_view_amount[1])):
                    pixels[obj_x + x][obj_y + y] = obj_color
    return pixels


def pixel_display(screen, screen_size, pixel_size, pixels, pixel_view_amount, dx, dy):
    '''
    draw pixels
    :param screen:
    :param screen_size: [screen_with, screen_height]
    :param pixels: 2 dimensional array with colors of pixels, we need to draw
    :param pixel_view_amount: how many pixels we want to draw [row length, column length]
    :param dx: offset of pixel net, related not int coords of camera
    :param dy:
    '''
    for row in range(pixel_view_amount[0]):
        for column in range(pixel_view_amount[1]):
            if pixels[row][column] != 0:
                pg.draw.rect(screen, pixels[row][column],
                             ((row - dx) * pixel_size, screen_size[1] - (column + 1 - dy) * pixel_size,
                              pixel_size + 1, pixel_size + 1))
            # we add +1 to pixel_size to fix empty place caused not int zoom


def scene_display(screen, objects, camera_pos, screen_size, zoom, background_color):
    '''
    main function that display scene using pixel_colorise(), draw_background(), pixel_display
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
    pixels = pixel_colorise(objects, camera_pos, pixel_view_amount)
    draw_background(screen, background_color, screen_size)
    pixel_display(screen, screen_size, pixel_size, pixels, pixel_view_amount, dx, dy)
