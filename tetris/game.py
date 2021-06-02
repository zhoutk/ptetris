# -*- coding: UTF-8 -*-

from tkinter.constants import ALL
from  tetris.config import UID, initGameRoom
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
        self.tetris = Tetris(self.canvas, 4, 0, self.nextTetris.getTetrisShape())
        for i in range(self.nextTetris.getRotateCount()):
            self.tetris.rotate()

        self.nextCanvas.delete(ALL)
        self.nextTetris = Tetris(self.nextCanvas, 1, 1, random.randint(0,6))
        for i in range(random.randint(0,4)):
            self.nextTetris.rotate()

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