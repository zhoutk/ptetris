# -*- coding: UTF-8 -*-
from tetris.config import *

class Block:
    def __init__(self, canvas, x, y, color = "red") -> None:
        self.canvas = canvas
        self.x = x
        self.y = y
        self.obj = canvas.create_rectangle((x - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, (y - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, x * BLOCKSIDEWIDTH + CANVASOFFSET, y * BLOCKSIDEWIDTH + CANVASOFFSET, fill = color, outline = "yellow")


    def relocate(self, detaX, detaY):
        self.canvas.move(self.obj, detaX * BLOCKSIDEWIDTH, detaY * BLOCKSIDEWIDTH)
        self.x += detaX
        self.y += detaY


    def clean(self):
        self.canvas.delete(self.obj)