import random


class color:

    def random():
        """
        :return: random color
        """
        rand_color = (int(256*random.random()), int(256*random.random()), int(256*random.random()))
        return rand_color
    PLAYER_COLOR = (135, 206, 235)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    UI = (150, 150, 150)
    UI2 = (70, 125, 100)