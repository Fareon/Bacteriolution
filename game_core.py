import play_units as unit
import game_manager as gm
import tricky_functions as f
import sound
import ui
import color

#INITIAL SHIT
cells = []
self_cells = []
food_generators = []
food = []
grid = [[ [] for _ in range(gm.scene_height)] for __ in range(gm.scene_width)]

def born_cell(pos, color, cell_type):
    new_cell = unit.Cell(pos[0], pos[1], color, cell_type)
    new_cell.change_food_source(food_generators)
    cells.append(new_cell)
    grid[pos[0]][pos[1]].append(new_cell)

def debug_grid():
    total_cells = 0
    for y in range(gm.scene_height):
        for x in range(gm.scene_width):
            for obj in grid[x][y]:
                if(obj.game_object == 'cell'): total_cells += 1
    print(total_cells)

def born_self_cell(pos, color, cell_type):
    new_cell = unit.Cell(pos[0], pos[1], color, cell_type)

    self_cells.append(new_cell)
    grid[pos[0]][pos[1]].append(new_cell)
    
    update_ui()

def born_food_gen(pos):
    food_gen = unit.FoodSource(pos, self_color=color.GREEN, food_color=color.BLUE)
    food_generators.append(food_gen)
    grid[pos[0]][pos[1]].append(food_gen)

def check_for_grid(cell):
    x, y = cell.x, cell.y
    radius = cell.r
    content = []

    for x_check in range(f.clamp(x - radius, 1, gm.scene_width-2), f.clamp(x + radius + 1, 1, gm.scene_width-2), 1):
        for y_check in range(f.clamp(y - radius, 1, gm.scene_width-2), f.clamp(y + radius + 1, 1, gm.scene_width-2), 1):
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
        cell.eat(list_of_cells, grid, food_eaten)
        if(cell.color == color.PLAYER_COLOR and food_eaten == all_food['food'][-1]):
            sound.play_eat_food_sound()
            update_ui()
            
    for food_eaten in all_food['cell']:
        if(cell.r > food_eaten.r):
            
            print('eaten cell')
            #if(food_eaten in grid[food_eaten.x][food_eaten.y]): 
            try:
                grid[food_eaten.x][food_eaten.y].remove(food_eaten)
            except:
                #delete_ghost_cells()
                debug_grid()
                print(len(cells) + len(self_cells))
                print(grid[food_eaten.x][food_eaten.y])
            if(food_eaten in cells): 
                cells.remove(food_eaten)
            if(food_eaten in self_cells): 
                self_cells.remove(food_eaten)
            
            cell.eat(list_of_cells, grid, food_eaten)
            if(cell.color == color.PLAYER_COLOR and food_eaten == all_food['cell'][-1]):
                sound.eat_cell_sound.play()
                update_ui()

def initialize_gameobjects():
    global cells, self_cells, food_generators, food, grid
    cells = []
    self_cells = []
    food_generators = []
    food = []
    grid = [[ [] for _ in range(gm.scene_height)] for __ in range(gm.scene_width)]

from random import randint
def generate_level(food_gens = 9, cells = 10, self_cells = 2):
    
    initialize_gameobjects()
    
    for i in range(food_gens):
        x_born = randint(3*gm.borders_width, gm.scene_width - 3*gm.borders_width)
        y_born = randint(3*gm.borders_width, gm.scene_height - 3*gm.borders_width)
        born_food_gen((x_born, y_born))

    for i in range(self_cells, self_cells + cells):
        x_born = randint(3*gm.borders_width, gm.scene_width - 3*gm.borders_width)
        y_born = randint(3*gm.borders_width, gm.scene_height - 3*gm.borders_width)
        born_cell([x_born, y_born], color.random_color(), i)

    for i in range(self_cells):
        x_born = randint(3*gm.borders_width, gm.scene_width - 3*gm.borders_width)
        y_born = randint(3*gm.borders_width, gm.scene_height - 3*gm.borders_width)
        born_self_cell([x_born, y_born], color.PLAYER_COLOR, i)

def delete_ghost_cells():
    for cell in cells:
        if(not (cell in grid[cell.x][cell.y])):
            cells.remove(cell)

def update_ui():
    #define maximum radius among self_cells
    if(len(self_cells) > 0):        
        max_r = 0
        for cell in self_cells:
            if(cell.r > max_r): max_r = cell.r
        
        ui.radius.text = "MAX RADIUS: " + str(max_r)
        ui.population.text = "Population: " + str(len(self_cells))
        ui.hunger.text = "HUNGER: " + str(self_cells[0].food_level)
        ui.speed.text = "SPEED: " + str(round(self_cells[0].velocity, 2) )
        
        ui.generate_text()
