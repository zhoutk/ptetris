# -*- coding: UTF-8 -*-

class Game:
    def __init__(self, canvas) -> None:
        self.canvas = canvas
        self.tetris = None
        self.nextTetris = None
        self.gameRoom = [[0 for i in range(12)] for i in range(22)]
        for i in range(22):
            self.gameRoom[i][0] = 1
            self.gameRoom[i][11] = 1
        for i in range(1, 12):
            self.gameRoom[21][i] = 1