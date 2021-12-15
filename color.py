from random import randint


def random_color():
    """
    :return: random color
    """
    rand_color = (randint(0, 255), randint(0, 255), randint(0, 255))
    return rand_color


PLAYER_COLOR = (135, 206, 235)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
UI = (150, 150, 150)
UI2 = (70, 125, 100)
INIT_PLAYER_COLOR = (135, 206, 235)

def rgb_to_hex(color): #as tuple (r, g, b)
    return '#{:02x}{:02x}{:02x}'.format(*color)
