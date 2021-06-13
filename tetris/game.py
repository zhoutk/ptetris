# -*- coding: UTF-8 -*-

from tkinter.constants import ALL
from  tetris.config import *
from tetris.tetris import Tetris
import random
from threading import Timer
import threading
import time
from tetris.dbdao.baseDao import *

class Game:
    def __init__(self, canvas, nextCanvas, app = None) -> None:
        self.app = app
        self.stepNum = 0
        self.dao = BaseDao()
        self.gameRunningStatus = 0
        self.canvas = canvas
        self.nextCanvas = nextCanvas
        self.tetris = None
        self.nextTetris = None
        self.worker = threading.Thread(target=self.opWork)
        self.worker.start()
        self.dbSaver = threading.Thread(target=self.dbSave)
        self.dbSaver.start()

    def opWork(self):
        while True:
            if not opQueue.empty():
                op = opQueue.get()
                if op == "Left":
                    self.moveLeft()
                elif op == "Right":
                    self.moveRight()
                elif op == "Up":
                    self.rotate()
                elif op == "Down":
                    self.moveDown()
                elif op == "space":
                    self.moveDownEnd()
                elif op == "quit":
                    break
            else:
                time.sleep(0.01)
        
    def dbSave(self):
        while True:
            if not dbQueue.empty():
                tablename,params = dbQueue.get()
                if tablename != "quit":
                    self.dao.insert(tablename, params)
                else:
                    break
            else:
                time.sleep(0.01)

    def start(self):
        self.gameRunningStatus = 1
        self.gameSpeedInterval = 1000
        self.gameSpeed = 1
        self.gameLevels = 0
        self.gameScores = 0
        self.stepNum = 0
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
            opQueue.put('Down')
            self.tick = Timer(self.gameSpeedInterval / 1000, self.tickoff)
            self.tick.start()


    def generateNext(self):
        self.stepNum += 1
        if self.gameRunningStatus == 1:
            dbQueue.put(("gameRecords",{
                "_id_":UID(), 
                "gameId":self.gameID,
                "blockType": self.tetris.getTetrisShape(),
                "rotateNumber": self.tetris.getRotateCount(),
                "LocateX": self.tetris.x,
                "LocateY": self.tetris.y,
                "stepId": self.stepNum,
                }))
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
            self.canvas.create_text(150, 200, text = "Game is over!", fill="white", font = "Times 28 italic bold")
            self.app.setStartButtonText("Start")
            print("game is over!")
            if self.gameRunningStatus == 1:
                dbQueue.put(("gameRecords",{
                    "_id_":UID(), 
                    "gameId":self.gameID,
                    "blockType": self.nextTetris.getTetrisShape(),
                    "rotateNumber": self.nextTetris.getRotateCount(),
                    "LocateX": 4,
                    "LocateY": 0,
                    "stepId": self.stepNum + 1,
                    }))
                dbQueue.put(("gameLists",{
                    "_id_":self.gameID, 
                    "speed": self.gameSpeed,
                    "levels": self.gameLevels,
                    "scores": self.gameScores,
                    "steps": self.stepNum + 1,
                    }))
            self.gameRunningStatus = 0
                
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
        if not self.tetris.moveDown():
            self.generateNext()
            rs = False
        return rs


    def moveDownEnd(self):
        while self.moveDown():
            pass

    def rotate(self):
        self.tetris.rotate()