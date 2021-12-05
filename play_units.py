from random import choices
from random import randint
import game_core as gc
import game_manager as gm
from color import color
import tricky_functions as f
from numpy import exp, cos, sin, array
from numpy.linalg import norm


class Cell:
    """
    This class is responsible for the cell itself, her movement and attributes
    """
    init_r = 2
    direct_list = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    init_velocity = 1
    init_vision_distance = 10
    game_object = 'food_gen'

    def __init__(self, x, y, cell_type):
        """
        :param x: horizontal position on the grid.py
        :param y: vertical position on the grid.py
        :param cell_type: type of a cell (contains color) (GREEN, for example)
        """
        self.x = x
        self.y = y
        self.cell_type = cell_type  # this is needed for future managing
        self.color = cell_type
        self.r = self.init_r
        self.direction = None  # will be a list of len 4 (up, right, down, left)
        self.velocity = self.init_velocity
        self.vision_distance = self.init_vision_distance
        self.energy = None  # In future will stand for hunger
        self.life = None  # In future will stand for how ling the cell is going to live
        self.food_level = 1

    def move(self, position: tuple):
        """
        Moves the cell according to its direction probabilities.
        Counts the weight of directions accordingly and moves the cell after choosing direction.
        :param grid: grid which defines the bonds
        :param position: tuple (len = 2), with coordinates of the most preferable direction
        """
        self.direction = [1 for _ in range(4)]  # FIXME: has to be normalized according to the coordinates
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
        food_koef = 1
        fear = 10
        heading_position = [self.x, self.y]
        if self.y + self.vision_distance >= len(grid):
            rows = grid[self.y - self.vision_distance:]
        elif self.y - self.vision_distance <= 0:
            rows = grid[:self.y + self.vision_distance]
        else:
            rows = grid[self.y - self.vision_distance:self.y + self.vision_distance]
        for row in rows:
            if self.x + self.vision_distance >= len(row):
                objects = grid[self.x - self.vision_distance:]
            elif self.x - self.vision_distance <= 0:
                objects = grid[:self.y + self.vision_distance]
            else:
                objects = grid[self.y - self.vision_distance:self.y + self.vision_distance]
            for dot in objects:
                for unit in dot:
                    if unit:
                        unit = unit[0]
                        if unit.cell_type != self.cell_type and unit.r > self.r:
                            heading_position[0] = self.x - (unit.x - self.x) * fear
                            heading_position[1] = self.y - (unit.y - self.y) * fear
                        elif (not cell_see_food) and unit.cell_type == 'food':  # FIXME: has to be edited in order to fit the model
                            heading_position[0] += int((unit.x - self.x) * food_koef)
                            heading_position[1] += int((unit.y - self.y) * food_koef)
                            cell_see_food = True
        if heading_position == [self.x, self.y]:
            heading_position = self.evaluate_foodsource(list_of_foodsources)
        for _ in range(2):
            if heading_position[_] < 0:
                heading_position[_] = 0
            elif heading_position[_] > len(grid):
                heading_position[_] = len(grid)
        return tuple(heading_position)

    def evaluate_foodsource(self, list_of_foodsources: list):
        """
        this function stands for the cell decision to move to a fodsource if no enemies are present
        :param list_of_foodsources: list of all foodsources on the map (objects). the cell decides to which one to go
        :return: heading position (list)
        """
        heading_position = [list_of_foodsources[0].x, list_of_foodsources[0].y]
        position = array([self.x, self.y])
        first_gen = array([list_of_foodsources[0].x, list_of_foodsources[0].y])
        for _ in range(1, len(list_of_foodsources)):
            gen_position = array([list_of_foodsources[_].x, list_of_foodsources[_].y])
            init_distance = norm(position - heading_position)
            distance = norm(position - gen_position)
            if distance < init_distance:
                heading_position = [list_of_foodsources[_].x, list_of_foodsources[_].y]
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
        self.range = 20
        self.rate = 0.1      #chance to generate food current frame
        self.color = color.GREEN

    def gen_food(self):

        r = (randint(4, self.range))**0.75
        angle = randint(0, 360)

        x_born = self.x + r*cos(angle)
        y_born = self.y + r * sin(angle)

        #x_born = self.x + (-1)**(randint(1,2)) * randint(2, self.range)
        #y_born = self.y + (-1) ** (randint(1, 2)) * randint(2, self.range)

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
