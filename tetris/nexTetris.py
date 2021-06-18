# -*- coding: UTF-8 -*-
from tetris.config import *
from tetris.nextBlock import *


class NexTetris:
    def __init__(self, shape):
        self.x = 1
        self.y = 1
        self.objs = nextCanvasBlocks
        self.rotateCount = 0
        self.shape = shape
        self.color = TETRISCOLORS[shape]
        self.data = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        index = 0
        curShape = TETRISAHPES[shape % len(TETRISAHPES)]
        for i, b in enumerate(curShape):
            if b:
                self.data[1 + i // TETRISDIMENSION][i % TETRISDIMENSION] = 1
                self.objs[index].configColor(self.color)
                self.objs[index].place(self.x + i % TETRISDIMENSION, self.y + 1 + i // TETRISDIMENSION)
                index += 1

    def getTetrisShape(self):
        return self.shape

    def getRotateCount(self):
        return self.rotateCount
    
    def rotate(self):
        for i in range(TETRISDIMENSION // 2):
            lenJ = TETRISDIMENSION - i - 1
            for j in range(i, lenJ):
                lenI = TETRISDIMENSION - j - 1
                t = self.data[i][j]
                self.data[i][j] = self.data[lenI][i]
                self.data[lenI][i] = self.data[lenJ][lenI]
                self.data[lenJ][lenI] = self.data[j][lenJ]
                self.data[j][lenJ] = t
        self.rotateCount += 1
        index = 0
        for i in range(TETRISDIMENSION):
            for j in range(TETRISDIMENSION):
                if self.data[i][j]:
                    self.objs[index].place(self.x + j, self.y + i)
                    index += 1