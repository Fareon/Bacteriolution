from random import choices
from random import randint
import game_core as gc
import game_manager as gm
from color import color
import tricky_functions as f
from numpy import cos, sin, array
from numpy.linalg import norm


def close(obj_1, obj_2, distance):
    obj_distance = (obj_1.x - obj_2.x) ** 2 + (obj_1.y - obj_2.y) ** 2
    return obj_distance < distance ** 2


def close_foodsource(cell, foodsources, distance):
    result = None
    for foodsource in foodsources:
        if close(cell, foodsource, distance):
            result = foodsource
            pass
    if result is not None:
        return result
    else:
        return False


class Cell:
    """
    This class is responsible for the cell itself, her movement and attributes
    """
    init_r = 2
    direct_list = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    init_velocity = 1
    init_vision_distance = 20
    game_object = 'food_gen'

    def __init__(self, x, y, cell_color, cell_type):
        """
        :param x: horizontal position on the grid.py
        :param y: vertical position on the grid.py
        :param color: color of a cell (GREEN, for example)
        """
        self.x = x
        self.y = y
        self.cell_type = cell_type  # this is needed for future managing
        self.color = cell_color
        self.r = self.init_r
        self.direction = None  # will be a list of len 4 (up, right, down, left)
        self.velocity = self.init_velocity
        self.vision_distance = self.init_vision_distance
        self.energy = None  # In future will stand for hunger
        self.life = None  # In future will stand for how ling the cell is going to live
        self.food_level = 1
        self.heading_position = None
        self.heading_foodsource = None

    def move(self, position: tuple):
        """
        Moves the cell according to its direction probabilities.
        Counts the weight of directions accordingly and moves the cell after choosing direction.
        :param grid: grid which defines the bonds
        :param position: tuple (len = 2), with coordinates of the most preferable direction
        """
        self.direction = [1 for _ in range(4)]  # FIXME: has to be normalized according to the coordinates
        if position[0] != self.x and position[1] != self.y:
            if position[0] >= self.x and position[1] >= self.y:
                self.direction[0] = position[1] - self.y
                self.direction[1] = position[0] - self.x
            elif position[0] >= self.x:
                self.direction[2] = self.y - position[1]
                self.direction[1] = position[0] - self.x
            elif position[1] >= self.y:
                self.direction[0] = position[1] - self.y
                self.direction[3] = self.x - position[0]
            else:
                self.direction[2] = self.y - position[1]
                self.direction[3] = self.x - position[0]
        if self.x <= self.r + 2:
            self.direction[3] = 0
        elif self.x >= len(gc.grid) - (self.r + 2):
            self.direction[1] = 0
        if self.y <= self.r + 2:
            self.direction[2] = 0
        elif self.y >= len(gc.grid[0]) - (self.r + 2):
            self.direction[0] = 0

        final_direction = choices(self.direct_list, weights=self.direction)[0]

        gc.grid[self.x][self.y].remove(self)

        self.x += final_direction[0] * self.velocity
        self.y += final_direction[1] * self.velocity

        gc.grid[self.x][self.y].append(self)

    #  Егор, пока что не реализцуй эту функцию,
    #  там надо прописать типы у всех типов, потому что это влияет на отпределение направления
    def evaluate_direction(self, grid: list, list_of_foodsources: list):
        """
        Evaluates the most preferable direction for a cell
        :param list_of_foodsources: list of all foodsources on the map (objects). the cell decides to which one to go.
        :param grid: map of objects on the playing surface
        :return: tuple of 2 ints -- position of direction
        """
        cell_see_food = False
        food_wish = 1
        fear = 10
        food_count = 0
        food_gen_count = 0
        cell_see_cell = False
        heading_position = [self.x, self.y]
        closest_foodsource = []
        if self.x + self.vision_distance >= len(grid):
            columns = grid[self.x - self.vision_distance:]
        elif self.x - self.vision_distance <= 0:
            columns = grid[:self.x + self.vision_distance]
        else:
            columns = grid[self.x - self.vision_distance:self.x + self.vision_distance]
        for row in columns:
            if self.y + self.vision_distance >= len(row):
                rows = grid[:self.y + self.vision_distance]
            elif self.y - self.vision_distance <= 0:
                rows = grid[self.y - self.vision_distance:]
            else:
                rows = grid[self.y - self.vision_distance:self.y + self.vision_distance]
            for dot in rows:
                for unit in dot:
                    if unit:
                        unit = unit[0]
                        if unit.cell_type != self.cell_type and unit.cell_type != "food" and unit.cell_type != "food_gen":
                            #print("see enemy", unit.cell_type)
                            #if unit.cell_type != self.cell_type: #and unit.r > self.r + 1 and unit.cell_type != "food":
                            heading_position[0] -= (unit.x - self.x)
                            heading_position[1] -= (unit.y - self.y)
                        #cell_see_food = True
                        #cell_see_cell = True
                        # elif unit.cell_type == 'food':  # FIXME: has to be edited in order to fit the model
                        # food_count += 1
                        # if not cell_see_food:
                        #  heading_position[0] += int((unit.x - self.x) * food_wish)
                        #  heading_position[1] += int((unit.y - self.y) * food_wish)
                        #  cell_see_food = True
                        # elif unit.cell_type == 'food_gen':
                        # food_gen_count += 1
                        # closest_foodsource = unit
        # if food_count <= 9 and food_gen_count != 0 and (not cell_see_cell):
        # heading_position = self.evaluate_foodsource(list_of_foodsources)
        return tuple(heading_position)

    def think_ahead(self, cells, foodsources, food):
        cell_see_foodsource = close(self, self.heading_foodsource, self.vision_distance // 3)
        heading_position = [self.x, self.y]
        cell_see_pray = False
        cell_see_enemy = False
        for cell in cells:
            if cell.cell_type != self.cell_type:
                if cell.r > self.r + 1:
                    if close(cell, self, self.vision_distance):
                        heading_position[0] -= (cell.x - self.x)
                        heading_position[1] -= (cell.y - self.y)
                        cell_see_enemy = True
                elif cell.r < self.r - 1:
                    if close(cell, self, self.vision_distance):
                        heading_position[0] += (cell.x - self.x)
                        heading_position[1] += (cell.y - self.y)
                        cell_see_pray = True
        if cell_see_enemy and close(self, self.heading_foodsource, self.vision_distance):
            self.evaluate_foodsource(foodsources)
            heading_position = [self.heading_foodsource.x, self.heading_foodsource.y]
        elif not cell_see_enemy:
            many_food = self.count_food(food)
            if not cell_see_foodsource:
                heading_position = [self.heading_foodsource.x, self.heading_foodsource.y]
            elif not many_food:
                self.evaluate_foodsource(foodsources)
                heading_position = [self.heading_foodsource.x, self.heading_foodsource.y]
            elif many_food:
                heading_position = self.get_food(food)
        return tuple(heading_position)

    def evaluate_foodsource(self, foodsources: list):
        """
        this function stands for the cell decision to move to a fodsource if no enemies are present
        :param foodsources: list of all foodsources on the map (objects). the cell decides to which one to go
        :return: heading position (list)
        """
        food_list = foodsources.copy()
        self.heading_foodsource = choices(food_list)[0]

    def count_food(self, food):
        count = 0
        for foodie in food:
            if close(self, foodie, self.vision_distance):
                count += 1
        if count >= 5:
            return True
        else:
            return False

    def get_food(self, food):
        for foodie in food:
            if close(self, foodie, self.vision_distance):
                heading_position = [foodie.x, foodie.y]
                pass
        return heading_position


    def mutate(self, mutate_probabilities):
        pass

    def tick(self):
        """
        Makes the cell grow older and become more hungry
        """
        self.energy -= 1
        self.life -= 1

    def grow(self):
        self.vision_distance += 2
        self.food_level = 1
        self.r += 1

    def eat(self):
        if self.food_level <= self.r ** 2:
            self.food_level += 1
        else:
            self.grow()


class FoodSource:
    """
    This class controls the position of a food source
    """
    cell_type = 'food_gen'
    game_object = 'food_gen'

    def __init__(self, position: tuple):
        self.x = position[0]
        self.y = position[1]
        self.r = 2
        self.range = 100
        self.rate = 0.03  # chance to generate food current frame
        self.color = color.GREEN

    def gen_food(self):
        r = (randint(4, self.range)) ** 0.75
        angle = randint(0, 360)

        x_born = self.x + r * cos(angle)
        y_born = self.y + r * sin(angle)

        # x_born = self.x + (-1)**(randint(1,2)) * randint(2, self.range)
        # y_born = self.y + (-1) ** (randint(1, 2)) * randint(2, self.range)

        x_born = f.clamp(x_born, 2, gm.scene_width - 3)
        y_born = f.clamp(y_born, 2, gm.scene_height - 3)

        new_food = Food((x_born, y_born))
        gc.food.append(new_food)
        gc.grid[x_born][y_born].append(new_food)


class Food:
    """
    This class controls food and its position
    """
    AMOUNT = 1
    cell_type = 'food'
    game_object = 'food'

    def __init__(self, food_position: tuple):
        self.x, self.y = self.position = food_position
        self.r = 1
        self.color = color.BLUE
