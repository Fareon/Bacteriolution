from random import choices


class Cell:
    """
    This class is responsible for the cell itself, her movement and attributes
    """
    init_r = 1
    direct_list = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    init_velocity = 1
    init_vision_distance = 10

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

    def move(self, position: tuple):
        """
        Moves the cell according to its direction probabilities.
        Counts the weight of directions accordingly and moves the cell after choosing direction.
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
        final_direction = choices(self.direct_list, weights=self.direction)[0]
        self.y += final_direction[1] * self.velocity
        self.x += final_direction[0] * self.velocity

    #  Егор, пока что не реализцуй эту функцию,
    #  там надо прописать типы у всех типов, потому что это влияет на отпределение направления
    def evaluate_direction(self, grid: list):
        """
        Evaluates the most preferable direction for a cell
        :param grid: map of objects on the playing surface
        :return: tuple of 2 ints -- position of direction
        """
        position = [self.x, self.y]
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
            for unit in objects:
                if unit is not None:
                    if unit.type == 'food':  # FIXME: has to be edited in order to fit the model
                        position[0] += unit.x - self.x
                        position[1] += unit.y - self.y
                    elif unit.cell_type != self.cell_type:
                        position[0] -= unit.x - self.x
                        position[1] -= unit.y - self.y
        return tuple(position)

    def mutate(self, mutate_probabilities):
        pass

    def tick(self):
        """
        Makes the cell grow older and become more hungry
        """
        self.energy -= 1
        self.life -= 1

    def grow(self):
        self.r += 1


class FoodSource:
    """
    This class controls the position of a food source
    """
    cell_type = 'food'

    def __init__(self, position: tuple):
        self.x = position[0]
        self.y = position[1]

    # def gen_food(self, food_position):
    # food_unit = Food(food_position)
    # return food_unit
    # пока что не нужный метод, может быть удален


class Food:
    """
    This class controls food and its position
    """
    AMOUNT = 1
    RADIUS = 1
    cell_type = 'food'

    def __init__(self, food_position: tuple):
        self.x, self.y = self.position = food_position
