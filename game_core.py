import numpy as np
import play_units as unit
import game_manager as gm
import ui
from color import color

#INITIAL SHIT
cells = []
self_cells = []
food_generators = []
food = []
grid = [[ [] for _ in range(gm.scene_height)] for __ in range(gm.scene_width)]

def born_cell(pos, color, cell_type):
    new_cell = unit.Cell(pos[0], pos[1], color, cell_type)
    new_cell.evaluate_foodsource(food_generators)
    cells.append(new_cell)
    grid[pos[0]][pos[1]].append(new_cell)

def born_self_cell(pos, color, cell_type):
    new_cell = unit.Cell(pos[0], pos[1], color, cell_type)

    self_cells.append(new_cell)
    grid[pos[0]][pos[1]].append(new_cell)
    
    update_ui()

def born_food_gen(pos):
    food_gen = unit.FoodSource(pos)
    food_generators.append(food_gen)
    grid[pos[0]][pos[1]].append(food_gen)

def check_for_food(point, radius):
    answer = []
    x, y = np.array(point).astype(int)
    content = []

    for x_check in range(x - radius, x + radius + 1, 1):
        for y_check in range(y - radius, y + radius + 1, 1):
            content += grid[x_check][y_check]

    for obj in content:
        if obj.game_object == 'food':
            answer.append(obj)
    return answer

def eat_food(cell, list_of_cells):
    x, y = cell.x, cell.y
    all_food = check_for_food((x, y), cell.r)
    for food_eaten in all_food:
        grid[food_eaten.x][food_eaten.y].remove(food_eaten)
        food.remove(food_eaten)
        cell.eat(list_of_cells)
        if(cell.color == color.PLAYER_COLOR):
            update_ui()

def update_ui():
    #define maximum radius among self_cells
    
    max_r = 0
    for cell in self_cells:
        if(cell.r > max_r): max_r = cell.r
    
    ui.radius.text = "MAX RADIUS: " + str(max_r)
    ui.population.text = "Population: " + str(len(self_cells))
    ui.hunger.text = "HUNGER: " + str(self_cells[0].food_level)
    ui.speed.text = "SPEED: " + str(round(self_cells[0].velocity, 1) )
    
    ui.generate_text()
