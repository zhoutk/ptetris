# -*- coding: UTF-8 -*-

from math import fabs
import tkinter
from tkinter.constants import ALL
from  tetris.config import *
from tetris.tetris import Tetris
import random
from threading import Timer
import threading
import time
from tetris.dbdao.baseDao import *
import copy

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
        self.records = []
        self.isAutoRunning = False

    def opWork(self):
        originTable = ""
        ps = []
        while True:
            if not opQueue.empty():
                cmd,data = opQueue.get()
                if cmd == "Left":
                    self.moveLeft()
                elif cmd == "Right":
                    self.moveRight()
                elif cmd == "Up":
                    self.rotate()
                elif cmd == "Down":
                    self.moveDown()
                elif cmd == "space":
                    self.moveDownEnd()
                elif cmd == "quit":
                    break
                elif cmd == "over":
                    self.dao.insertBatch(originTable, ps)
                    originTable = ""
                    ps.clear()
                elif cmd == "save":
                    tablename,params = data
                    if originTable == "":
                        originTable = tablename
                    if originTable != tablename  or len(ps) > 10:
                        savePs = copy.deepcopy(ps)
                        Timer(0, self.doSaveRecords,(originTable, savePs)).start()
                        ps.clear()
                        originTable = tablename
                    ps.append(params)
                elif cmd == "setauto":
                    self.isAutoRunning = data
                elif cmd == "pause":
                    self.gameRunningStatus = data
                elif cmd == "autonext": 
                    if self.gameRunningStatus == 1 and self.isAutoRunning == 1:
                        self.autoProcessCurBlock()
                        self.generateNext()
                    self.tick = Timer(AUTOINTERVAL, self.tickoff)
                    self.tick.start()
            else:
                time.sleep(WORKINTERVAL)
    
    def doSaveRecords(self, tablename, ps):
        self.dao.insertBatch(tablename, ps)

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

        self.tick = Timer(self.gameSpeedInterval * (0 if self.isAutoRunning else 1) / 1000, self.tickoff)
        self.tick.start()


    def playback(self, gameID):
        rs = self.dao.select("gameRecords",{"gameId":gameID,"sort":"stepId"},["blockType","rotateNumber","LocateX","LocateY","stepId"])
        self.records = rs.get("rows")

        self.gameRunningStatus = 2
        self.gameSpeedInterval = 1000
        self.gameSpeed = 1
        self.gameLevels = 0
        self.gameScores = 0
        self.stepNum = 1
        self.app.updateGameInfo(1,0,0)
        self.canvas.delete(ALL)
        self.nextCanvas.delete(ALL)
        initGameRoom()

        if len(self.records) > 2:
            blockType,rotateNumber,self.LocateX,self.LocateY,stepId = self.records[0]
            self.tetris = Tetris(self.canvas, 4, 0,blockType)
            for i in range(rotateNumber % 4):
                self.tetris.rotate()
            blockType,rotateNumber,LocateX,LocateY,stepId = self.records[1]
            self.nextTetris = Tetris(self.nextCanvas, 1, 1, blockType)
            for i in range(rotateNumber % 4):
                self.nextTetris.rotate()
            self.tick = Timer(BACKINTERVAL, self.tickoff)
            self.tick.start()
        else:
            self.app.setButtonStartState(tkinter.ACTIVE)
            self.app.setButtonPlayBackState(tkinter.ACTIVE)

    def pause(self):
        opQueue.put(("pause",5))

    def resume(self):
        self.gameRunningStatus = 1  
        self.tick = Timer(self.gameSpeedInterval * (0 if self.isAutoRunning else 1) / 1000, self.tickoff)
        self.tick.start()      

    def tickoff(self):
        if self.gameRunningStatus == 1:
            if self.isAutoRunning:
                opQueue.put(("autonext",()))
            else:
                opQueue.put(('Down',()))
                self.tick = Timer(self.gameSpeedInterval / 1000, self.tickoff)
                self.tick.start()
        elif self.gameRunningStatus == 2:
            self.tetris.relocate(self.LocateX, self.LocateY)
            self.tetris.fixTetrisInGameRoom()
            self.generateNext()
            self.tick = Timer(BACKINTERVAL, self.tickoff)
            self.tick.start()

    def generateNext(self):
        if self.gameRunningStatus == 1 or self.gameRunningStatus == 2:
            self.stepNum += 1
            if self.gameRunningStatus == 1:
                opQueue.put(("save",("gameRecords",{
                    "_id_":UID(), 
                    "gameId":self.gameID,
                    "blockType": self.tetris.getTetrisShape(),
                    "rotateNumber": self.tetris.getRotateCount(),
                    "LocateX": self.tetris.x,
                    "LocateY": self.tetris.y,
                    "stepId": self.stepNum,
                    })))
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
                if not self.tetris.rotate(False):
                    break
            if self.tetris.canPlace(4, 0):
                self.nextCanvas.delete(ALL)
                initRotate = 0
                if self.gameRunningStatus == 1:
                    self.nextTetris = Tetris(self.nextCanvas, 1, 1, random.randint(0,6))
                    initRotate = random.randint(0,4)
                else:
                    blockType,rotateNumber,self.LocateX,self.LocateY,stepId = self.records[self.stepNum - 1]
                    self.tetris.relocate(self.LocateX, self.tetris.y)
                    blockType,rotateNumber,LocateX,LocateY,stepId = self.records[self.stepNum]
                    self.nextTetris = Tetris(self.nextCanvas, 1,1, blockType)
                    initRotate = rotateNumber
                for i in range(initRotate):
                    self.nextTetris.rotate(False)
            else:
                self.canvas.create_text(150, 200, text = "Game is over!", fill="white", font = "Times 28 italic bold")
                self.app.setStartButtonText("Start")
                print("game is over!")
                if self.gameRunningStatus == 1:
                    opQueue.put(("save",("gameRecords",{
                        "_id_":UID(), 
                        "gameId":self.gameID,
                        "blockType": self.nextTetris.getTetrisShape(),
                        "rotateNumber": self.nextTetris.getRotateCount(),
                        "LocateX": 4,
                        "LocateY": 0,
                        "stepId": self.stepNum + 1,
                        })))
                    opQueue.put(("save",("gameLists",{
                        "_id_":self.gameID, 
                        "speed": self.gameSpeed,
                        "levels": self.gameLevels,
                        "scores": self.gameScores,
                        "steps": self.stepNum + 1,
                        })))
                    opQueue.put(("over",()))
                self.gameRunningStatus = 0
                self.app.setButtonStartState(tkinter.ACTIVE)
                self.app.setButtonPlayBackState(tkinter.ACTIVE)
                
    def getGameRunningStatus(self):
        return self.gameRunningStatus

    def clearRows(self, noTry = None):
        noTry = True if noTry == None else noTry
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
        if len(occupyLines) > 0 and noTry:
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

    def evaluate(self, t : Tetris):
        ct = t.y
        cct = self.clearRows(False)
        if cct > 1:
            ct += 10 * (cct - 1)
        for i in range(TETRISDIMENSION):
            for j in range(TETRISDIMENSION):
                if t.data[i][j]:
                    ct += 1 if t.hasBlock(t.x + j + 1, t.y + i) else 0
                    ct += 1 if t.hasBlock(t.x + j - 1, t.y + i) else 0
                    ct += 1 if t.hasBlock(t.x + j, t.y + i + 1) else 0
                    ct += 1 if t.hasBlock(t.x + j, t.y + i - 1) else 0

                    if i == 3 or t.data[i + 1][j] == 0:
                        if not t.hasBlock(t.x + j, t.y + i + 1):
                            ct -=4
                        else:
                            k = 2
                            while t.y + i + k <= 20:
                                if not t.hasBlock(t.x, t.y + i + k):
                                    ct -= 1
                                    break
                                k += 1
        return ct

    def autoProcessCurBlock(self):
        max = 0
        initX = self.tetris.x
        initY = self.tetris.y
        goalX = 0
        goalY = 0
        tmp = Tetris(self.canvas,initX,initY,self.tetris.getTetrisShape(),False)
        rct = self.tetris.getRotateCount() % 4
        for _ in range(rct):
            tmp.rotate(False, False)
        rct = 0
        for r in range(4):
            if r > 0:
                tmp.relocate(initX, initY)
                tmp.rotate(False, False)
            while tmp.moveLeft(False):
                pass
            flag = True
            while flag:
                while tmp.moveDown(False):
                    pass
                tmp.fixTetrisInGameRoom()
                score = self.evaluate(tmp)
                tmp.unfixTetrisInGameRoom()
                if score > max:
                    max = score
                    goalX = tmp.x
                    goalY = tmp.y
                    rct = r
                elif score == max:
                    if random.randint(0,2) == 1:
                        goalX = tmp.x
                        goalY = tmp.y
                        rct = r
                tmp.relocate(tmp.x, initY)
                flag = tmp.moveRight(False)
        for _ in range(rct):
            self.tetris.rotate(False)
        self.tetris.relocate(goalX, goalY)
        self.tetris.fixTetrisInGameRoom()