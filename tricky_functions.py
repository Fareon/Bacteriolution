from random import random


def clamp(number, minimum: int, maximum: int):
    """
    'Cuts' the number between maximum and minimum, and turns it into integer
    :param number: given number
    :param minimum: minimum
    :param maximum: maximum
    :return: int (cut number)
    """
    if number < minimum:
        return minimum
    elif number > maximum:
        return maximum
    else:
        return int(number)


def chance(probability):
    """
    Function for probabilities
    :param probability: given probability
    :return: bool
    """
    destiny = random()  # from 0 to 1
    if destiny <= probability:
        return True
    else:
        return False
