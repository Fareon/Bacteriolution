from play_units import Cell, FoodSource
from game_manager import scene_width, scene_height, borders_width
from tricky_functions import clamp
from sound import eat_cell_sound, play_eat_food_sound
from ui import Radius, Population, Hunger, Speed, generate_text
from color import random_color, GREEN, BLUE, INIT_PLAYER_COLOR
from random import randint

cells = []
self_cells = []
food_generators = []
food = []
grid = [[[] for _ in range(scene_height)] for __ in range(scene_width)]


def born_cell(pos, cell_color, cell_type):
    """
    Create computer cells
    :param pos: position of a created cell
    :param cell_color: color of the cell
    :param cell_type: cell type
    """
    new_cell = Cell(pos[0], pos[1], cell_color, cell_type)
    new_cell.change_food_source(food_generators)
    cells.append(new_cell)
    grid[pos[0]][pos[1]].append(new_cell)


def debug_grid():
    total_cells = 0
    for y in range(scene_height):
        for x in range(scene_width):
            for obj in grid[x][y]:
                if obj.game_object == 'cell':
                    total_cells += 1
    print(total_cells)


def born_self_cell(pos, cell_color, cell_type):
    """
    Create user cells
    :param pos: position of a created cell
    :param cell_color: color of the cell
    :param cell_type: cell type
    """
    new_cell = Cell(pos[0], pos[1], cell_color, cell_type)
    self_cells.append(new_cell)
    grid[pos[0]][pos[1]].append(new_cell)
    update_ui()


def born_food_gen(pos):
    """
    Create a food generator
    :param pos: position of a created food generator
    """
    food_gen = FoodSource(pos, self_color=GREEN, food_color=BLUE)
    food_generators.append(food_gen)
    grid[pos[0]][pos[1]].append(food_gen)


def check_for_grid(cell):
    x, y = cell.x, cell.y
    radius = cell.r
    content = []

    for x_check in range(clamp(x - radius, 1, scene_width - 2), clamp(x + radius + 1, 1, scene_width - 2), 1):
        for y_check in range(
                clamp(y - radius, 1, scene_width - 2),
                clamp(y + radius + 1, 1, scene_width - 2),
                1
        ):
            content += grid[x_check][y_check]

    keys = ['food', 'cell', 'food_gen']
    values = [[] for _ in keys]
    answer = dict(zip(keys, values))

    for obj in content:
        if obj.game_object == 'food':
            answer['food'].append(obj)
        if obj.game_object == 'cell' and obj.color != cell.color:
            answer['cell'].append(obj)

    return answer


def eat_food(cell, list_of_cells):
    """
    Function that stands for eating during the game
    :param cell: given cell
    :param list_of_cells: list of cells of the same playing type
    """
    all_food = check_for_grid(cell)

    for food_eaten in all_food['food']:
        grid[food_eaten.x][food_eaten.y].remove(food_eaten)
        food.remove(food_eaten)
        cell.eat(list_of_cells, grid, food_eaten)
        if cell.cell_type == 0 and food_eaten == all_food['food'][-1]:
            play_eat_food_sound()
            update_ui()

    for food_eaten in all_food['cell']:
        if cell.r > food_eaten.r:
            try:
                grid[food_eaten.x][food_eaten.y].remove(food_eaten)
            except:
                debug_grid()
                print(len(cells) + len(self_cells))
                print(grid[food_eaten.x][food_eaten.y])
            if food_eaten in cells:
                cells.remove(food_eaten)
            if food_eaten in self_cells:
                self_cells.remove(food_eaten)

            cell.eat(list_of_cells, grid, food_eaten)
            if cell.cell_type == 0 and food_eaten == all_food['cell'][-1]:
                eat_cell_sound.play()
                update_ui()


def initialize_game_objects():
    """
    Initializing storage for game objects
    """
    global cells, self_cells, food_generators, food, grid
    cells = []
    self_cells = []
    food_generators = []
    food = []
    grid = [[[] for _ in range(scene_height)] for __ in range(scene_width)]


def generate_level(food_gens=9, number_of_cells=10, number_of_self_cells=2):
    """
    This function generates a map with all the objects
    :param food_gens: number of food generators
    :param number_of_cells: number of enemy cells
    :param number_of_self_cells: number of your own cells
    """
    initialize_game_objects()

    for _ in range(food_gens):
        x_born = randint(3 * borders_width, scene_width - 3 * borders_width)
        y_born = randint(3 * borders_width, scene_height - 3 * borders_width)
        born_food_gen((x_born, y_born))

    for _ in range(1, 1 + number_of_cells):
        x_born = randint(3 * borders_width, scene_width - 3 * borders_width)
        y_born = randint(3 * borders_width, scene_height - 3 * borders_width)
        born_cell([x_born, y_born], random_color(), _)

    for _ in range(number_of_self_cells):
        x_born = randint(3 * borders_width, scene_width - 3 * borders_width)
        y_born = randint(3 * borders_width, scene_height - 3 * borders_width)
        born_self_cell([x_born, y_born], INIT_PLAYER_COLOR, 0)


def update_ui():
    """
    Updating user interface
    """
    # Define maximum Radius among self_cells
    if len(self_cells) > 0:
        max_r = 0
        for cell in self_cells:
            if cell.r > max_r:
                max_r = cell.r

    # Define maximum velocity among self_cells
    if len(self_cells) > 0:
        max_vel = 0
        for cell in self_cells:
            if cell.velocity > max_vel:
                max_vel = cell.velocity

        Radius.text = "MAX RADIUS: " + str(max_r)
        Population.text = "Population: " + str(len(self_cells))
        Hunger.text = "SELFISHNESS: " + str(self_cells[0].direct_constant)
        Speed.text = "MAX SPEED: " + str(round(self_cells[0].velocity, 2))

        generate_text()
