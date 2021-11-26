import numpy as np
import play_units as unit

#INITIAL SHIT
cells = []
food = []
food_sources = []

def born_cell(pos, color):
    cells.append(unit.Cell(pos[0], pos[1], color))

def born_food_source(pos):
    food_sources.append(unit.FoodSource(pos))
