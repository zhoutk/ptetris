# -*- coding: UTF-8 -*-

from tkinter.constants import ALL
from  tetris.config import *
from tetris.tetris import Tetris
import random
from threading import Timer

class Game:
    def __init__(self, canvas, nextCanvas, app = None) -> None:
        self.app = app
        self.gameRunningStatus = 0
        self.canvas = canvas
        self.nextCanvas = nextCanvas
        self.tetris = None
        self.nextTetris = None

    def start(self):
        self.gameRunningStatus = 1
        self.gameSpeedInterval = 1000
        self.gameSpeed = 1
        self.gameLevels = 0
        self.gameScores = 0
        self.app.updateGameInfo(1,0,0)
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

        self.tick = Timer(self.gameSpeedInterval / 1000, self.tickoff)
        self.tick.start()


    def pause(self):
        self.gameRunningStatus = 5

    def resume(self):
        self.gameRunningStatus = 1  
        self.tick = Timer(self.gameSpeedInterval / 1000, self.tickoff)
        self.tick.start()      

    def tickoff(self):
        if self.gameRunningStatus == 1:
            self.moveDown()
            self.tick = Timer(self.gameSpeedInterval / 1000, self.tickoff)
            self.tick.start()


    def generateNext(self):
        cleanLevels = self.clearRows()
        if cleanLevels > 0:
            self.gameLevels += cleanLevels
            self.gameScores += SCORES[cleanLevels]
            if self.gameScores / STEPUPSCORE >= self.gameSpeed:
                self.gameSpeed += 1
                self.gameSpeedInterval -= STEPUPINTERVAL
            self.app.updateGameInfo(self.gameSpeed, self.gameLevels, self.gameScores)
        
        self.tetris = Tetris(self.canvas, 4, 0, self.nextTetris.getTetrisShape())
        for i in range(self.nextTetris.getRotateCount()):
            if not self.tetris.rotate():
                break

        if self.tetris.canPlace(4, 0):
            self.nextCanvas.delete(ALL)
            self.nextTetris = Tetris(self.nextCanvas, 1, 1, random.randint(0,6))
            for i in range(random.randint(0,4)):
                self.nextTetris.rotate()
        else:
            self.gameRunningStatus = 0
            self.canvas.create_text(150, 200, text = "Game is over!", fill="white", font = "Times 28 italic bold")
            print("game is over!")

    def getGameRunningStatus(self):
        return self.gameRunningStatus

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
                break
            h -= 1
        if len(occupyLines) > 0:
            self.doCleanRows(occupyLines)
        return len(occupyLines)

    def doCleanRows(self, lines):
        index = 0
        h = lines[index]
        while h >= 0:
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
        rs = True
        curTetrisLock.acquire()
        try:
            if not self.tetris.moveDown():
                self.generateNext()
                rs = False
        finally:
            curTetrisLock.release()
        return rs


    def moveDownEnd(self):
        while self.moveDown():
            pass

    def rotate(self):
        self.tetris.rotate()