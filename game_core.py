import numpy as np
import play_units as unit
import game_manager as gm

#INITIAL SHIT
cells = []
food_generators = []
food = []
grid = [[ [] for _ in range(gm.scene_height)] for __ in range(gm.scene_width)]

def born_cell(pos, color):
    new_cell = unit.Cell(pos[0], pos[1], color)
    cells.append(new_cell)
    grid[pos[0]][pos[1]].append(new_cell)

def born_food_gen(pos):
    food_gen = unit.FoodSource(pos)
    food_generators.append(food_gen)
    grid[pos[0]][pos[1]].append(food_gen)

def check_for_food(point, radius):
    answer = []
    x, y = point
    content = []

    for x_check in range(x - radius, x + radius + 1, 1):
        for y_check in range(y - radius, y + radius + 1, 1):
            content += grid[x_check][y_check]

    for obj in content:
        if obj.game_object == 'food':
            answer.append(obj)

    return answer

def eat_food(cell):
    x, y = cell.x, cell.y
    all_food = check_for_food((x, y), cell.r)
    for food in all_food:
        grid[food.x][food.y].remove(food)
        cell.grow()
