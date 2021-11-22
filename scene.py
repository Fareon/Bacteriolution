def pixel_blit(screen, objects, camera_pos, screen_param, pixel_view_amount):
    '''
    we chose color for pixels, that we want to draw (pixels in camera area)
    and then draw them

    Object coords should be given as int (pixel have 1x1 dimension)
    Camera coords are in the same coordinate system, but can be float
    :param screen:
    :param objects: list with objects we want to draw
    :param camera_pos: coords of camera [x, y]
    :param screen_param: [screen_with, screen height]
    :param pixel_view_amount: how many pixels we want to draw [string length, column length]
    '''
    pixel_width = screen_param[0] / pixel_view_amount[0]
    pixel_height = screen_param[1] / pixel_view_amount[1]
    int_camera_coords = []
    int_camera_coords.append(int(camera_pos[0]))
    int_camera_coords.append(int(camera_pos[1]))
    scene_objects = []  # list of objects, located in camera area
    for obj in objects:
        x = obj.x - int_camera_coords[0]
        y = obj.y - int_camera_coords[1]
        r = obj.r
        if ((abs(x) <= screen_param[0] / 2 + r) and (abs(y) <= screen_param[1] / 2 + r)):
            scene_objects.append(
                [int(x + (pixel_view_amount[0]) / 2), int(y + (pixel_view_amount[1]) / 2), r, obj.color])
            # there are objects in new system of coords in this list
    pixels = [[[255, 255, 255] for i in range(pixel_view_amount[0] + 1)]
              for j in range(pixel_view_amount[1] + 1)]  # creating list of pixels
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
    # now we draw all pixels
    dx = camera_pos[0] - int_camera_coords[0]
    dy = camera_pos[1] - int_camera_coords[1]
    string_number = 0
    column_number = 0
    for string in pixels:
        for column in string:
            x = pg.draw.rect(screen, column,
                             ((string_number - dx) * pixel_width,
                              screen_param[1] - (column_number + 1 - dy) * pixel_height,
                              pixel_width, pixel_height))
            column_number += 1
        column_number = 0
        string_number += 1
