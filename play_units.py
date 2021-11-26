from random import choices


class Cell:
    """
    This class is responsible for the cell itself, her movement and attributes
    """
    init_r = 1
    direct_list = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    init_velocity = 1

    def __init__(self, x, y, cell_type):
        """
        :param x: horizontal position on the grid
        :param y: vertical position on the grid
        :param cell_type: type of a cell (contains color) (GREEN, for example)
        """
        self.x = x
        self.y = y
        self.type = cell_type  # this is needed for future managing
        self.color = cell_type
        self.r = self.init_r
        self.direction = None  # will be a list of len 4 (up, right, down, left)
        self.velocity = self.init_velocity

    def move(self, position: tuple):
        """
        Moves the cell according to its direction probabilities.
        Counts the weight of directions accordingly and moves the cell after choosing direction.
        :param position: tuple (len = 2), with coordinates of the most preferable direction
        """
        self.direction = [1, 1, 1, 1]  # FIXME: has to be normalized according to the coordinates
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

    def mutate(self, mutate_probabilities):
        pass

    def grow(self):
        self.radius += 1


class FoodSource:
    """
    This class controls the position of a food source
    """

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

    def __init__(self, food_position: tuple):
        self.x, self.y = self.position = food_position
