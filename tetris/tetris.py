# -*- coding: UTF-8 -*-
from tetris.config import *
from tetris.block import *


class Tetris:
    def __init__(self, canvas, x, y, shape):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.objs = []
        self.rotateCount = 0
        self.shape = shape
        self.color = TETRISCOLORS[shape]
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
                self.objs.append(Block(canvas, self.x + i % TETRISDIMENSION, self.y + 1 + i // TETRISDIMENSION, self.color))

    def getTetrisShape(self):
        return self.shape

    def getRotateCount(self):
        return self.rotateCount
    
    def hasBlock(self, x, y):
        if x < 1 or x > 10 or y > 20:
            return True
        if GameRoom[y][x] == 1:
            return True
        else:
            return False
    
    def canPlace(self, x, y):
        print("entry canPlace, ", x, y)
        for i in range(TETRISDIMENSION):
            for j in range(TETRISDIMENSION):
                if self.data[i][j] and GameRoom[y + i][x + j]:
                    print("rs canPlace false, ", x, y)
                    return False
        print("rs canPlace true, ", x, y)
        return True

    def moveLeft(self):
        if self.canPlace(self.x - 1, self.y):
            self.relocate(self.x - 1, self.y)

    def moveRight(self):
        if self.canPlace(self.x + 1, self.y):
            self.relocate(self.x + 1, self.y)

    def moveUp(self):
        self.relocate(self.x, self.y - 1)

    def moveDown(self):
        print("enter tetris' down one line.")
        if self.canPlace(self.x, self.y + 1):
            self.relocate(self.x, self.y + 1)
            print("down one line, ", self.x, self.y)
            return True
        else:
            for i in range(TETRISDIMENSION):
                for j in range(TETRISDIMENSION):
                    if self.data[i][j]:
                        GameRoom[self.y + i][self.x + j] = 1
            return False

    def rotate(self):
        for i in range(TETRISDIMENSION // 2):
            lenJ = TETRISDIMENSION - i - 1
            for j in range(i, lenJ):
                lenI = TETRISDIMENSION - j - 1
                if self.data[i][j] and self.hasBlock(self.x + lenJ, self.y + j) or \
                    self.data[lenI][i] and self.hasBlock(self.x + j, self.y + i) or \
                    self.data[lenJ][lenI] and self.hasBlock(self.x + i, self.y + lenI) or \
                    self.data[j][lenJ] and self.hasBlock(self.x + lenI, self.y + lenJ):
                    return False
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
        self.redraw()
        return True

    def redraw(self):
        self.clean()
        for i in range(TETRISDIMENSION):
            for j in range(TETRISDIMENSION):
                if self.data[i][j]:
                    self.objs.append(Block(self.canvas, self.x + j, self.y + i, self.color))

    def relocate(self, x, y):
        print("entry relocate, ", x, y)
        for block in self.objs:
            print("entry block loop, ", block.x, block.y)
            block.relocate(x - self.x, y - self.y)
        self.x = x
        self.y = y
        print("rs relocate, ", x, y)

    def clean(self):
        for block in self.objs:
            block.clean()
        self.objs.clear()