class Cell:
    init_r = 1

    def __init__(self, x, y, cell_type):
        self.x = x
        self.y = y
        self.type = cell_type
        self.radius = init_r
        self.velocity = None

    def move(self, velocity):
        pass

    def mutate(self, mutate_probabilities):
        pass

    def grow(self):
        self.radius += 1


class FoodSource:

    def __init__(self, position: tuple):
        self.x = position[0]
        self.y = position[1]

    def gen_food(self):
        pass