from random import choices, randint
from numpy import cos, sin
from color import color
import tricky_functions as f


def close(obj_1, obj_2, distance):
    """
    This function is needed to understand whether the two given objects are closer than the given distance
    :param obj_1: First object
    :param obj_2: Second object
    :param distance: The distance needed to be evaluated
    :return: True if closer, False else
    """
    obj_distance = (obj_1.x - obj_2.x) ** 2 + (obj_1.y - obj_2.y) ** 2
    return obj_distance < distance ** 2


class Cell:
    """
    This class is responsible for the cell itself, her movement and attributes
    """
    init_r = 2
    direct_list = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    init_velocity = 1.
    init_vision_distance = 20
    game_object = 'cell'
    init_split_radius = 6
    init_direct_constant = 2
    mutating_parameters = [init_r, init_velocity, init_vision_distance, init_split_radius, init_direct_constant]

    def __init__(self,
                 x,
                 y,
                 cell_color,
                 cell_type,
                 velocity=None,
                 vision_distance=None,
                 split_radius=None,
                 after_split_r=None
                 ):
        """
        Initializes the creation of an object of class Cell
        :param x: horizontal position on the grid.py
        :param y: vertical position on the grid.py
        :param cell_color: color of a cell (GREEN, for example)
        :param cell_type: Type of a newly born cell
        :param velocity: Cell's velocity
        :param vision_distance: Parameter, that defines how far the cell cen see
        :param split_radius: Radius, which is needed to be reached before splitting
        :param after_split_r: Radius of the daughter cells
        """
        self.x = x
        self.y = y
        self.color = cell_color
        self.cell_type = cell_type

        if after_split_r is None:
            self.after_split_r = self.init_r
        else:
            self.after_split_r = after_split_r

        if velocity is None:
            self.velocity = self.init_velocity
        else:
            self.velocity = velocity

        if vision_distance is None:
            self.vision_distance = self.init_vision_distance
        else:
            self.vision_distance = vision_distance

        if split_radius is None:
            self.split_radius = self.init_split_radius
        else:
            self.split_radius = split_radius

        self.r = self.init_r
        self.food_level = 1
        self.heading_food_source = None
        self.direct_constant = self.init_direct_constant
        self.life = None  # In future will stand for how ling the cell is going to live
        self.energy = None  # In future will stand for hunger

    def move(self, position: tuple, grid):
        """
        Moves the cell according to its direction probabilities and coordinates.
        Counts the weight of directions accordingly and moves the cell after choosing direction.
        :param grid: grid which defines the bonds
        :param position: tuple (len = 2), with coordinates of the most preferable direction
        """
        # Removing the cell from grid
        grid[self.x][self.y].remove(self)

        direction = [self.direct_constant for _ in range(4)]
        # Counting probabilities
        if position[0] != self.x and position[1] != self.y:
            if position[0] >= self.x and position[1] >= self.y:
                direction[0] = position[1] - self.y
                direction[1] = position[0] - self.x
            elif position[0] >= self.x:
                direction[2] = self.y - position[1]
                direction[1] = position[0] - self.x
            elif position[1] >= self.y:
                direction[0] = position[1] - self.y
                direction[3] = self.x - position[0]
            else:
                direction[2] = self.y - position[1]
                direction[3] = self.x - position[0]

        # Moving the cell while the impulse is not zero
        impulse = self.velocity
        while impulse >= 1:
            if self.x <= self.r + 2:
                direction[3] = 0
            elif self.x >= len(grid) - (self.r + 2):
                direction[1] = 0
            if self.y <= self.r + 2:
                direction[2] = 0
            elif self.y >= len(grid[0]) - (self.r + 2):
                direction[0] = 0

            final_direction = choices(self.direct_list, weights=direction)[0]

            self.x += final_direction[0]
            self.y += final_direction[1]

            impulse -= 1

        if impulse > 0:
            if bool(choices([0, 1], weights=[1 - impulse, impulse])[0]):
                if self.x <= self.r + 2:
                    direction[3] = 0
                elif self.x >= len(grid) - (self.r + 2):
                    direction[1] = 0
                if self.y <= self.r + 2:
                    direction[2] = 0
                elif self.y >= len(grid[0]) - (self.r + 2):
                    direction[0] = 0

                final_direction = choices(self.direct_list, weights=direction)[0]

                self.x += final_direction[0]
                self.y += final_direction[1]

        # Returning the cell to the grid
        grid[self.x][self.y].append(self)

    def think_ahead(self, cells, food_sources, food):
        """
        This method defines the position, which cell is heading to
        :param cells: List of all cells on the map
        :param food_sources: List of all food sources on the map
        :param food: List of all food on the map
        :return: The most preferable heading position (tuple of len 2)
        """
        cell_see_food_source_close = close(self, self.heading_food_source, self.vision_distance // 3)
        cell_see_food_source_far = close(self, self.heading_food_source, self.vision_distance + 5)
        heading_position = [self.x, self.y]
        cell_see_pray = False
        cell_see_enemy = False
        for cell in cells:
            if cell.cell_type != self.cell_type:
                if cell.r > self.r:
                    if close(cell, self, self.vision_distance):
                        heading_position[0] -= (cell.x - self.x)
                        heading_position[1] -= (cell.y - self.y)
                        cell_see_enemy = True
                elif cell.r < self.r - 1:
                    if close(cell, self, self.vision_distance - 5):
                        cell_see_pray = True
                        pray = cell
        if cell_see_enemy and cell_see_food_source_far:
            self.change_food_source(food_sources)
            heading_position = [self.heading_food_source.x, self.heading_food_source.y]
        elif (not cell_see_enemy) and (not cell_see_pray):
            many_food = self.count_food(food)
            if not cell_see_food_source_far:
                heading_position = [self.heading_food_source.x, self.heading_food_source.y]
            elif not many_food:
                self.change_food_source(food_sources)
                heading_position = [self.heading_food_source.x, self.heading_food_source.y]
            elif many_food:
                heading_position = self.get_food(food)
        elif cell_see_pray and (not cell_see_enemy):
            heading_position[0] += (pray.x - self.x)
            heading_position[1] += (pray.y - self.y)
        return tuple(heading_position)

    def change_food_source(self, food_sources: list):
        """
        Changes the food source the cell if heading for
        :param food_sources: List of all food sources on the map (objects). The cell decides which to reach
        """
        self.heading_food_source = choices(food_sources)[0]

    def count_food(self, food):
        """
        This method helps the cell to count the food within the visible distance
        :param food: List of all food on the map
        :return: True if enough food, else False
        """
        count = 0
        for foodie in food:
            if close(self, foodie, self.vision_distance + 10):
                count += 1
        return count >= 5

    def get_food(self, food):
        """
        Gives the cell a destination of a food object
        :param food:  List of all food on the map
        :return: position, which to head (list, len = 2)
        """
        heading_position = None
        for foodie in food:
            if close(self, foodie, self.vision_distance + 10):
                heading_position = [foodie.x, foodie.y]
                pass
        return heading_position

    def split_cell(self, cells, grid):
        """
        The cell splits and becomes the two new ones
        :param cells: List of cells of the game
        :param grid: Game grid
        """
        self.r = self.after_split_r

        # Creating new object of the type Cell
        daughter = Cell(self.x,
                        self.y,
                        self.color,
                        self.cell_type,
                        velocity=self.velocity,
                        vision_distance=self.vision_distance,
                        split_radius=self.split_radius,
                        after_split_r=self.after_split_r
                        )
        daughter.heading_food_source = self.heading_food_source
        daughter.mutate()

        # Appending the cell where needed
        cells.append(daughter)
        grid[daughter.x][daughter.y].append(daughter)

    def mutate(self):
        """
        This method changes characteristics of a given cell accordingly to built in constants.
        """
        mutating_parameter = choices(self.mutating_parameters, weights=[3, 3, 1, 3, 2])[0]
        if mutating_parameter == self.mutating_parameters[0]:
            if self.after_split_r <= 2:
                self.after_split_r += choices([0, 1], weights=[1, 3])[0]
            else:
                self.after_split_r += choices([-1, 1], weights=[1, 3])[0]
        elif mutating_parameter == self.mutating_parameters[1]:
            if self.velocity <= 1:
                self.velocity += randint(1, 10) / 10
            else:
                self.velocity += randint(-10, 10) / 10
        elif mutating_parameter == self.mutating_parameters[2]:
            if self.vision_distance <= 10:
                self.vision_distance += choices([0, 2], weights=[1, 2])[0]
            else:
                self.vision_distance += choices([-2, 2], weights=[1, 2])[0]
        elif mutating_parameter == self.mutating_parameters[3]:
            if self.split_radius <= self.after_split_r:
                self.split_radius += choices([0, 1], weights=[1, 3])[0]
            else:
                self.split_radius += choices([-1, 1], weights=[1, 3])[0]
        elif mutating_parameter == self.mutating_parameters[4]:
            if self.direct_constant <= 1:
                self.direct_constant += randint(0, 1)
            else:
                self.direct_constant += choices([-1, 1])[0]

    def grow(self):
        """
        The cell grows in radius
        """
        self.food_level = 1
        self.r += 1

    def eat(self, cells, grid, eaten_object):
        """
        The cell eats the object and grows.
        :param cells: List of all cells on the map
        :param grid: Grid of the game
        :param eaten_object: The object the cell eats
        """
        if self.food_level <= self.r ** 2:
            self.food_level += eaten_object.r
        else:
            self.grow()

        if self.r >= self.split_radius:
            self.split_cell(cells, grid)


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
        self.range = 50
        self.rate = 0.03  # chance to generate food current frame
        self.color = color.GREEN

    def gen_food(self, scene_width, scene_height, grid, food):
        r = (randint(4, self.range)) ** 0.75
        angle = randint(0, 360)

        x_born = self.x + r * cos(angle)
        y_born = self.y + r * sin(angle)

        # x_born = self.x + (-1)**(randint(1,2)) * randint(2, self.range)
        # y_born = self.y + (-1) ** (randint(1, 2)) * randint(2, self.range)

        x_born = f.clamp(x_born, 2, scene_width - 3)
        y_born = f.clamp(y_born, 2, scene_height - 3)

        new_food = Food((x_born, y_born))
        food.append(new_food)
        grid[x_born][y_born].append(new_food)


class Food:
    """
    This class controls food and its position
    """
    cell_type = 'food'
    game_object = 'food'

    def __init__(self, food_position: tuple):
        self.x, self.y = self.position = food_position
        self.r = 1
        self.color = color.BLUE
