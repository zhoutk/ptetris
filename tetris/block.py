# -*- coding: UTF-8 -*-
from tetris.config import *

class Block:
    def __init__(self, canvas, x, y, color = "red") -> None:
        self.canvas = canvas
        self.x = x
        self.y = y
        self.obj = canvas.create_rectangle((x - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, (y - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, x * BLOCKSIDEWIDTH + CANVASOFFSET, y * BLOCKSIDEWIDTH + CANVASOFFSET, fill = color, outline = "yellow")


    def relocate(self, detaX, detaY):
        print("entry block relocate, ", self.x, self.y, self.obj, detaX * BLOCKSIDEWIDTH, detaY * BLOCKSIDEWIDTH)
        self.canvas.move(self.obj, detaX * BLOCKSIDEWIDTH, detaY * BLOCKSIDEWIDTH)
        print("move block relocate, ", self.x, self.y)
        self.x += detaX
        self.y += detaY


    def clean(self):
        self.canvas.delete(self.obj)