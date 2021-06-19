# -*- coding: UTF-8 -*-
from tetris.config import *
from tetris.config import blockQueue, SCREENOFFSET

class Block:
    def __init__(self, canvas, x, y, color = "red") -> None:
        self.canvas = canvas
        self.x = x
        self.y = y
        if blockQueue.empty():
            self.obj = canvas.create_rectangle((x - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, (y - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, \
                x * BLOCKSIDEWIDTH + CANVASOFFSET, y * BLOCKSIDEWIDTH + CANVASOFFSET, fill = color, outline = "yellow")
            allCanvasBlocks.append(self.obj)
            TetrisCounter[0] += 1
            # print("create block count ----------------- ", TetrisCounter[0])
        else:
            self.obj = blockQueue.get()
            canvas.coords(self.obj, (x - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, (y - 1) * BLOCKSIDEWIDTH + CANVASOFFSET, \
                x * BLOCKSIDEWIDTH + CANVASOFFSET, y * BLOCKSIDEWIDTH + CANVASOFFSET)
            canvas.itemconfig(self.obj, fill = color)

    def relocate(self, detaX, detaY):
        self.canvas.move(self.obj, detaX * BLOCKSIDEWIDTH, detaY * BLOCKSIDEWIDTH)
        self.x += detaX
        self.y += detaY


    def clean(self):
        self.canvas.move(self.obj, SCREENOFFSET, 0)
        blockQueue.put(self.obj)