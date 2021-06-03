# -*- coding: UTF-8 -*-

from tkinter.constants import ALL
from  tetris.config import *
from tetris.tetris import Tetris
import random

class Game:
    def __init__(self, canvas, nextCanvas) -> None:
        self.canvas = canvas
        self.nextCanvas = nextCanvas
        self.tetris = None
        self.nextTetris = None

    def start(self):
        self.canvas.delete(ALL)
        self.nextCanvas.delete(ALL)
        initGameRoom()

        self.gameID = UID()
        self.tetris = Tetris(self.canvas, 4, 0, random.randint(0,6))
        for i in range(random.randint(0,4)):
            self.tetris.rotate()
        self.nextTetris = Tetris(self.nextCanvas, 1, 1, random.randint(0,6))
        for i in range(random.randint(0,4)):
            self.nextTetris.rotate()

    def generateNext(self):
        cleanLevels = self.clearRows()
        
        self.tetris = Tetris(self.canvas, 4, 0, self.nextTetris.getTetrisShape())
        for i in range(self.nextTetris.getRotateCount()):
            self.tetris.rotate()

        self.nextCanvas.delete(ALL)
        self.nextTetris = Tetris(self.nextCanvas, 1, 1, random.randint(0,6))
        for i in range(random.randint(0,4)):
            self.nextTetris.rotate()

    def clearRows(self):
        occupyLines = []
        h = 20
        while h > 0:
            allOccupy = 0
            for i in range(1, 11):
                if GameRoom[h][i]:
                    allOccupy += 1
            if allOccupy == 10:
                occupyLines.append(h)
            elif allOccupy == 0:
                if len(occupyLines) > 0:
                    self.doCleanRows(occupyLines)
                break
            h -= 1
        return len(occupyLines)

    def doCleanRows(self, lines):
        index = 0
        h = lines[index]
        while h > 0:
            if index < len(lines) and h == lines[index]:
                index += 1
                for j in range(1, 11):
                    GameRoom[h][j] = 0
                    for b in self.canvas.find_closest(j * BLOCKSIDEWIDTH - HALFBLOCKWIDTH, h  * BLOCKSIDEWIDTH - HALFBLOCKWIDTH):
                        self.canvas.delete(b)
            else:
                count = 0
                for j in range(1, 11):
                    if GameRoom[h][j] == 1:
                        count += 1
                        GameRoom[h + index][j] = GameRoom[h][j]
                        GameRoom[h][j] = 0
                        for b in self.canvas.find_closest(j * BLOCKSIDEWIDTH - HALFBLOCKWIDTH, h  * BLOCKSIDEWIDTH - HALFBLOCKWIDTH):
                            self.canvas.move(b, 0, index * BLOCKSIDEWIDTH)
                if count == 0:
                    break
            h -= 1

    def moveLeft(self):
        self.tetris.moveLeft()

    def moveRight(self):
        self.tetris.moveRight()

    def moveDown(self):
        if not self.tetris.moveDown():
            self.generateNext()
            return False
        else:
            return True

    def moveDownEnd(self):
        while self.moveDown():
            pass

    def rotate(self):
        self.tetris.rotate()