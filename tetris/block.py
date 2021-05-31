# -*- coding: UTF-8 -*-
from tetris.config import *

class Block:
    def __init__(self, canvas, x, y) -> None:
        self.canvas = canvas
        self.x = x
        self.y = y
        self.obj = canvas.create_rectangle((x - 1) * BLOCKSIDEWIDTH, (y - 1) * BLOCKSIDEWIDTH, x * BLOCKSIDEWIDTH, y * BLOCKSIDEWIDTH, fill = "blue")


    def relocate(self, x, y):
        self.canvas.move(self.obj, (x - self.x) * BLOCKSIDEWIDTH, (y - self.y) * BLOCKSIDEWIDTH)
        self.x = x
        self.y = y