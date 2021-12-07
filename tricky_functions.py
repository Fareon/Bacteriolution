from numpy import random


def clamp(x, a, b):
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return int(x)


def chance(probability):
    destiny = random.rand()  # from 0 to 1
    if destiny <= probability:
        return True
    else:
        return False
