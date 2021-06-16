# -*- coding: UTF-8 -*-
from time import time
import tkinter
from tetris.game import Game
from tkinter import *
from tkinter import ttk
from tetris.block import *
import time
from tetris.dbdao.baseDao import *

def start():
    initDb()
    # dao = BaseDao()
    # # rs = dao.select("gameLists",{"page": 1, "size":2, "levels":1, "ins":["speed", "5"]})
    # rs = dao.select("gameLists",{"page": 1, "size":2,"sort":"levels desc"}, ["_id_"])
    # print(rs)
    # rs = dao.update("gameLists",{"_id_": "139866","speed": 5, "levels": 1, "scores": 2})
    # rs = dao.insertBatch("gameLists",[{"_id_": "939866","speed": 6},{"_id_": "139866","speed": 9}])

    root = Tk()
    root.title("Tetris")
    root.geometry('470x630')
    root.resizable(0, 0)
    App(root)
    root.mainloop()


def initDb():
    dao = BaseDao()
    dao.execSql("CREATE TABLE IF NOT EXISTS 'gameRecords' ('_id_' text NOT NULL PRIMARY KEY,\
			'gameId' text NOT NULL, 'blockType' integer NOT NULL,\
			'rotateNumber' integer DEFAULT 0,'LocateX' integer NOT NULL,'LocateY' integer NOT NULL,\
			'stepId' integer NOT NULL, 'create_time' text DEFAULT (datetime('now','localtime')));")
    dao.execSql("CREATE TABLE IF NOT EXISTS 'gameLists' ('_id_' text NOT NULL PRIMARY KEY,\
        'speed' integer DEFAULT 1,'levels' integer DEFAULT 0,'scores' integer DEFAULT 0,\
        'steps' integer DEFAULT 0,'create_time' text DEFAULT (datetime('now','localtime')));")


class App:
    def __init__(self,root):
        root.protocol('WM_DELETE_WINDOW', lambda arg=root: self.rootClose(arg))

        self.gameCanvas = Canvas(root, bg='black', height=600 + CANVASOFFSET * 2, width=300 + CANVASOFFSET * 2)
        self.gameCanvas.place(x=12, y=10)

        self.nextCanvas = Canvas(root, bg='black', height=120 + CANVASOFFSET * 2, width=120 + CANVASOFFSET * 2)
        self.nextCanvas.place(x = 330, y = 10)

        frame = Frame(root)
        frame.place(x = 330, y = 160)

        Label(frame, text="STEPS:").pack(anchor="w")
        self.stepsVar = StringVar()
        Label(frame, height=1, width=12, relief=SUNKEN, bd=1, textvariable=self.stepsVar).pack(anchor="w")

        Label(frame, text = "SPEED:").pack(anchor="w")
        self.speedVar = StringVar()
        speed = Label(frame, height=1, width=12, relief=SUNKEN, bd=1, textvariable=self.speedVar)
        speed.pack(anchor="w")

        Label(frame, text = "LEVELS:").pack(anchor="w")
        self.levelsVar = StringVar()
        levels = Label(frame, height=1, width=12, relief=SUNKEN, bd=1, textvariable=self.levelsVar)
        levels.pack(anchor="w")

        Label(frame, text = "SCORES:").pack(anchor="w")
        self.scoresVar = StringVar()
        scores = Label(frame, height=1, width=12, relief=SUNKEN, bd=1, textvariable=self.scoresVar)
        scores.pack(anchor="w")

        Label(frame, text = "").pack(anchor="w")
        self.autoVal = tkinter.IntVar()
        Checkbutton(frame, text = "AutoPlay",variable=self.autoVal, onvalue=1,offvalue=0,command=self.checkboxClicked).pack(anchor="w")
        self.btnStartVar = StringVar()
        self.btnStartVar.set("Start")
        self.btnStart = Button(frame, height=1, width=10, command=self.btnStartClicked, textvariable=self.btnStartVar)
        self.btnStart.pack(anchor="w")

        Label(frame, text = "").pack(anchor="w")
        coboxVar = StringVar
        cobox = ttk.Combobox(frame, textvariable=coboxVar, height=5, width=8, state="readonly")
        cobox.pack(anchor="w")
        cobox["value"] = ("last", "one", "two", "three")
        cobox.current(0)
        cobox.bind("<<ComboboxSelected>>", self.comboxClicked)
        self.cobox = cobox
        self.btnPlayBack = Button(frame, text = "PlayBack", height=1, width=10, command = self.btnPlaybackClicked)
        self.btnPlayBack.pack(anchor="w")

        self.gameCanvas.bind(sequence="<Key>", func=self.processKeyboardEvent)
        self.game = Game(self.gameCanvas, self.nextCanvas, self)
        self.gameCanvas.focus_set()

    
    def checkboxClicked(self):
        opQueue.put(("setauto",self.autoVal.get()))
        self.gameCanvas.focus_set()

    def processKeyboardEvent(self, ke):
        if self.game.getGameRunningStatus() == 1 and self.game.isAutoRunning == 0:
            if ke.keysym == 'Left':
                opQueue.put(('Left',()))
            if ke.keysym == 'Right':
                opQueue.put(('Right',()))
            if ke.keysym == 'Up':
                opQueue.put(('Up',()))
            if ke.keysym == 'Down':
                opQueue.put(('Down',()))
            if ke.keysym == 'space':
                opQueue.put(('space',()))

    def setButtonStartState(self, status):
        self.btnStart.config(state = status)

    def setButtonPlayBackState(self, status):
        self.btnPlayBack.config(state = status)

    def updateGameInfo(self, speed, levels, scores):
        self.speedVar.set(speed)
        self.levelsVar.set(levels)
        self.scoresVar.set(scores)

    def setStartButtonText(self, text):
        self.btnStartVar.set(text)

    def btnStartClicked(self):
        self.btnPlayBack.config(state = tkinter.DISABLED)
        if self.game.getGameRunningStatus() == 0:
            self.btnStartVar.set("Pause")
            self.game.start()
        elif self.game.getGameRunningStatus() == 1:
            self.btnStartVar.set("Resume")
            self.game.pause()
        elif self.game.getGameRunningStatus() == 5:
            self.btnStartVar.set("Pause")
            self.game.resume()
        self.gameCanvas.focus_set()


    def btnPlaybackClicked(self):
        self.btnStart.config(state = tkinter.DISABLED)
        self.btnPlayBack.config(state = tkinter.DISABLED)
        lastID = ""
        params = {"size":1}
        if self.cobox.get() == "one":
            params["sort"] = "scores desc"
            params["page"] = 1
        elif self.cobox.get() == "two":
            params["sort"] = "scores desc"
            params["page"] = 2
        elif self.cobox.get() == "three":
            params["sort"] = "scores desc"
            params["page"] = 3
        else:
            params["sort"] = "create_time desc"
            params["page"] = 1
        rs = self.game.dao.select("gameLists", params, ["_id_"])
        if rs.get("code") and rs.get("code") == 200:
            lastID = rs.get("rows")[0][0]
        if len(lastID) > 0:
            self.game.playback(lastID)
        else:
            self.btnStart.config(state = tkinter.ACTIVE)
            self.btnPlayBack.config(state = tkinter.ACTIVE)
        self.gameCanvas.focus_set()


    def comboxClicked(self, event):
        print(self.cobox.get())
        print("combobox ... ")
        self.gameCanvas.focus_set()


    def rootClose(self, root):
        print("timer close.")
        if hasattr(self.game, "tick"):
            self.game.tick.cancel()
        opQueue.put(("quit",()))
        time.sleep(0.3)
        root.quit()