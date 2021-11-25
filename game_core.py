import numpy as np
import play_units as unit

#INITIAL SHIT
cells = []

def born_cell(pos, color):
    cells.append(unit.Cell(pos[0], pos[1], color))