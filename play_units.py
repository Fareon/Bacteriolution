from random import choices

direct_list = [1, 1, -1, -1]


class Cell:
    """
    This class is responsible for the cell itself, her movement and attributes
    """
    init_r = 1
    init_velocity = 1

    def __init__(self, x, y, cell_type):
        """
        :param x: horizontal position on the grid
        :param y: vertical position on the grid
        :param cell_type: type of a cell (contains color) (GREEN, for example)
        """
        self.x = x
        self.y = y
        self.type = cell_type
        self.radius = self.init_r
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
            self.direction[2] = position[1] - self.y
            self.direction[1] = position[0] - self.x
        elif position[1] >= self.y:
            self.direction[0] = position[1] - self.y
            self.direction[3] = position[0] - self.x
        else:
            self.direction[2] = position[1] - self.y
            self.direction[3] = position[0] - self.x
        final_direction = direct_list[self.direction.index(choices(self.direction, weights=self.direction))]
        if final_direction / 2 == 0:
            self.y += self.velocity * final_direction
        else:
            self.x += self.velocity * final_direction

    def mutate(self, mutate_probabilities):
        pass

    def grow(self):
        self.radius += 1


class FoodSource:

    def __init__(self, position: tuple):
        self.x = position[0]
        self.y = position[1]

    # def gen_food(self, food_position):
    # food_unit = Food(food_position)
    # return food_unit
    # пока что не нужный метод, может быть удален


class Food:
    AMOUNT = 1
    RADIUS = 1

    def __init__(self, food_position: tuple):
        self.position = food_position
