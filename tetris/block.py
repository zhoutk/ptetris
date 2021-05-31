# -*- coding: UTF-8 -*-
from tetris.config import *

class Block:
    def __init__(self, canvas, x, y, color = "red") -> None:
        self.canvas = canvas
        self.x = x
        self.y = y
        self.obj = canvas.create_rectangle((x - 1) * BLOCKSIDEWIDTH, (y - 1) * BLOCKSIDEWIDTH, x * BLOCKSIDEWIDTH, y * BLOCKSIDEWIDTH, fill = color)


    def relocate(self, detaX, detaY):
        self.canvas.move(self.obj, detaX * BLOCKSIDEWIDTH, detaY * BLOCKSIDEWIDTH)
        self.x += detaX
        self.y += detaY


    def clean(self):
        self.canvas.delete(self.obj)