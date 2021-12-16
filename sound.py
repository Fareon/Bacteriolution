import pygame as pg

pg.init()
pg.mixer.music.load('sounds/background_music.wav')
eat_food_sound = pg.mixer.Sound('sounds/eat_food_sound.wav')
eat_cell_sound = pg.mixer.Sound('sounds/eat_cell_sound.wav')


def play_background_music():
    """
    Plays background music
    """
    pg.mixer.music.play(-1)


def play_eat_food_sound():
    """
    Plays food eating sound
    """
    eat_food_sound.play()


def play_eat_cell_sound():
    """
    Plays cell eating sound
    """
    eat_cell_sound.play()


def shut_down_music():
    """
    Shuts down all sounds
    """
    pg.mixer.music.pause()
    eat_food_sound.set_volume(0)
