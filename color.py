from random import randint

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
UI = (150, 150, 150)
UI2 = (70, 125, 100)
INIT_PLAYER_COLOR = (135, 206, 235)


def random_color():
    """
    :return: random color
    """
    rand_color = (randint(0, 255), randint(0, 255), randint(0, 255))
    return rand_color


def rgb_to_hex(color: tuple):
    """
    Turns a color in RGB format into the same one in the HEX format
    :param color: tuple of len 2, RGB color
    :return: color in hex format
    """
    return '#{:02x}{:02x}{:02x}'.format(*color)
