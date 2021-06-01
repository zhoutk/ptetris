# -*- coding: UTF-8 -*-
from tetris.config import *
from tetris.block import *


class Tetris:
    def __init__(self, canvas, x, y, shape, color="red"):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.objs = []
        self.rotateCount = 0
        self.color = color
        self.data = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        curShape = TETRISAHPES[shape % len(TETRISAHPES)]
        for i, b in enumerate(curShape):
            if b:
                self.data[1 + i // TETRISDIMENSION][i % TETRISDIMENSION] = 1
                self.objs.append(Block(canvas, self.x + i % TETRISDIMENSION, self.y + 1 + i // TETRISDIMENSION, color))

    def moveLeft(self):
        self.relocate(self.x - 1, self.y)

    def moveRight(self):
        self.relocate(self.x + 1, self.y)

    def moveUp(self):
        self.relocate(self.x, self.y - 1)

    def moveDown(self):
        self.relocate(self.x, self.y + 1)

    def rotate(self):
        for i in range(len(self.data)):
            for j in range(i+1, len(self.data)):
                temp = self.data[i][j]
                self.data[i][j] = self.data[j][i]
                self.data[j][i] = temp
        self.rotateCount += 1
        self.clean()
        for i in range(TETRISDIMENSION):
            for j in range(TETRISDIMENSION):
                if self.data[i][j]:
                    self.objs.append(Block(self.canvas, self.x + j, self.y + i, self.color))


    def relocate(self, x, y):
        for block in self.objs:
            block.relocate(x - self.x, y - self.y)
        self.x = x
        self.y = y

    def clean(self):
        for block in self.objs:
            block.clean()
        self.objs.clear()
