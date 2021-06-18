# -*- coding: UTF-8 -*-
from tetris.config import *
from tetris.config import blockQueue, SCREENOFFSET

class NextBlock:
    def __init__(self, canvas, x, y, color) -> None:
        self.canvas = canvas
        self.obj = canvas.create_rectangle((x - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, (y - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, \
            x * BLOCKSIDEWIDTH + CANVASOFFSET, y * BLOCKSIDEWIDTH + CANVASOFFSET, fill = color, outline = "yellow")
            

    def place(self, newX, newY):
        self.canvas.coords(self.obj, (newX - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, (newY - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, \
            newX * BLOCKSIDEWIDTH + CANVASOFFSET, newY * BLOCKSIDEWIDTH + CANVASOFFSET)

    def configColor(self, color):
        self.canvas.itemconfig(self.obj, fill = color)