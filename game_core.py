import numpy as np
import play_units as unit
import game_manager as gm

#INITIAL SHIT
cells = []
food_generators = []
food = []
grid = [[None for _ in range(gm.scene_height)] for __ in range(gm.scene_width)]

def born_cell(pos, color):
    new_cell = unit.Cell(pos[0], pos[1], color)
    cells.append(new_cell)
    grid[pos[0]][pos[1]] = new_cell

def born_food_gen(pos):
    food_gen = unit.FoodSource(pos)
    food_generators.append(food_gen)
    grid[pos[0]][pos[1]] = food_gen
