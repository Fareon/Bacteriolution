class Grid:
    """
    Gathers the information about objects in order to draw them after
    """
    def __int__(self, grid_size=(1000, 1000)):
        """
        Inits the grid and loads it with nones
        :param grid_size: tuple if len 2 and type int. Size of the grid
        """
        self.massive = [[None for _ in range(grid_size[0])] for __ in range(grid_size[1])]

    def update(self):
        """
        Updates the data according to objects in play_units.py
        :return:
        """
        pass
