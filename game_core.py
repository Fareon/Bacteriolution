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

def check_for_grid(cell):
    x, y = cell.x, cell.y
    radius = cell.r
    content = []

    for x_check in range(x - radius, x + radius + 1, 1):
        for y_check in range(y - radius, y + radius + 1, 1):
            content += grid[x_check][y_check]
    
    keys = ['food', 'cell', 'food_gen']
    values = [[] for i in keys]
    answer = dict(zip(keys, values))
    
    for obj in content:
        if obj.game_object == 'food':
            answer['food'].append(obj)
        if (obj.game_object == 'cell' and obj.color != cell.color):
            answer['cell'].append(obj)
            #print('found cell')
    
    return answer

def eat_food(cell, list_of_cells):
    x, y = cell.x, cell.y
    all_food = check_for_grid(cell)
    for food_eaten in all_food['food']:
        grid[food_eaten.x][food_eaten.y].remove(food_eaten)
        food.remove(food_eaten)
        cell.eat(list_of_cells)
        if(cell.color == color.PLAYER_COLOR and food_eaten == all_food['food'][-1]):
            update_ui()
            
    for food_eaten in all_food['cell']:
        if(cell.r > food_eaten.r):
            
            print('eaten cell')
            
            grid[food_eaten.x][food_eaten.y].remove(food_eaten)
            if(food_eaten in cells): cells.remove(food_eaten)
            if(food_eaten in self_cells): self_cells.remove(food_eaten)
            cell.eat(list_of_cells)
            if(cell.color == color.PLAYER_COLOR and food_eaten == all_food['cell'][-1]):
                update_ui()
                
            print('Cells: ',len(cells))
            print('Player cells: ',len(self_cells))

def update_ui():
    #define maximum radius among self_cells
    
    max_r = 0
    for cell in self_cells:
        if(cell.r > max_r): max_r = cell.r
    
    ui.radius.text = "MAX RADIUS: " + str(max_r)
    ui.population.text = "Population: " + str(len(self_cells))
    ui.hunger.text = "HUNGER: " + str(self_cells[0].food_level)
    ui.speed.text = "SPEED: " + str(round(self_cells[0].velocity, 2) )
    
    ui.generate_text()
