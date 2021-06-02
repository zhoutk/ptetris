# -*- coding: UTF-8 -*-

from tkinter.constants import ALL
from  tetris.config import UID
from tetris.tetris import Tetris
import random

class Game:
    def __init__(self, canvas, nextCanvas) -> None:
        self.canvas = canvas
        self.nextCanvas = nextCanvas
        self.tetris = None
        self.nextTetris = None
        self.gameRoom = [[0 for i in range(12)] for i in range(22)]
        for i in range(22):
            self.gameRoom[i][0] = 1
            self.gameRoom[i][11] = 1
        for i in range(1, 12):
            self.gameRoom[21][i] = 1

    def start(self):
        self.canvas.delete(ALL)
        self.nextCanvas.delete(ALL)
        self.gameID = UID()
        self.tetris = Tetris(self.canvas, 4, 0, random.randint(0,6))
        self.nextTetris = Tetris(self.nextCanvas, 1, 1, random.randint(0,6))

    def moveLeft(self):
        self.tetris.moveLeft()

    def moveRight(self):
        self.tetris.moveRight()

    def moveDown(self):
        self.tetris.moveDown()

    def rotate(self):
        self.tetris.rotate()
