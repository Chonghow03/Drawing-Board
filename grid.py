from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import *
class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0


    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
# Initialise the self.brush_size with the value self.DEFAULT_BRUSH_SIZE
# Initialise the self.grid with class ArrayR(x)
        self.brush_size = self.DEFAULT_BRUSH_SIZE
        self.grid = ArrayR(x)

# If the draw_style is "SET", applying the class SetLayerStore() on each grid square.
# The first for loop is to apply ArrayR with the dimension y to all the rows of grid.
# The second for loop is to apply SetLayerStore() to every grid square.
        if draw_style == "SET":
            for row in range(x):
                self.grid[row]=ArrayR(y)
                for column in range(y):
                    self.grid[row][column] = SetLayerStore()

# If the draw_style is "ADD", applying the class AdditiveLayerStore() on each grid square.
# The first for loop is to apply ArrayR with the dimension y to all the rows of grid.
# The second for loop is to apply AdditiveLayerStore() to every grid square.
        elif draw_style == "ADD":
            for row in range(x):
                self.grid[row]=ArrayR(y)
                for column in range(y):
                    self.grid[row][column] = AdditiveLayerStore()

# If the draw_style is "SEQUENCE", applying the class SequenceLayerStore() on each grid square.
# The first for loop is to apply ArrayR with the dimension y to all the rows of grid.
# The second for loop is to apply SequenceLayerStore() to every grid square.
        else:
            for row in range(x):
                self.grid[row]=ArrayR(y)
                for column in range(y):
                    self.grid[row][column] = SequenceLayerStore()

    def __getitem__(self, index):
        return self.grid[index]

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
# First, checking the brush size is at maximum size or not.
# If the brush size is smaller than maximum brush size, brush size added by 1, otherwise do nothing.
        if self.brush_size<self.MAX_BRUSH:
            self.brush_size+=1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
# This function is the inverse of the increase_brush_size.
# First, checking the brush size is at minimum size or not.
# If the brush size is larger than maximum brush size, brush size subtracted by 1, otherwise do nothing.
        if self.brush_size>self.MIN_BRUSH:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
# To activate the special affect on all grid squares,it required to find all the grid squares by using 2 for loops
# The first loop is to determine the rows part of the grid and the second for loop is to find the columns part of grid
# For instance, the first grid square is self.grid[0][0], then second is self.grid[0][1],
# until self.grid[len(self,grid)][self.grid[0]]
# Every grid squares, I apply the special effect by calling special function in layer store class.
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.grid[i][j].special()   #Call layerstore special


