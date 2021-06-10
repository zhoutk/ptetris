# -*- coding: UTF-8 -*-
from time import time
from tetris.game import Game
from tkinter import *
from tkinter import ttk
from tetris.block import *
import time
from tetris.dbdao.baseDao import *

def start():
    initDb()
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
        Checkbutton(frame, text = "AutoPlay").pack(anchor="w")
        self.btnStartVar = StringVar()
        self.btnStartVar.set("Start")
        Button(frame, height=1, width=10, command=self.btnStartClicked, textvariable=self.btnStartVar).pack(anchor="w")

        Label(frame, text = "").pack(anchor="w")
        coboxVar = StringVar
        cobox = ttk.Combobox(frame, textvariable=coboxVar, height=5, width=8, state="readonly")
        cobox.pack(anchor="w")
        cobox["value"] = ("last", "one", "two", "three")
        cobox.current(0)
        cobox.bind("<<ComboboxSelected>>", self.comboxClicked)
        self.cobox = cobox
        Button(frame, text = "PlayBack", height=1, width=10, command = self.btnPlaybackClicked).pack(anchor="w")

        self.gameCanvas.bind(sequence="<Key>", func=self.processKeyboardEvent)
        self.game = Game(self.gameCanvas, self.nextCanvas, self)
        self.gameCanvas.focus_set()

    
    def processKeyboardEvent(self, ke):
        if self.game.getGameRunningStatus() == 1:
            if ke.keysym == 'Left':
                opQueue.put('Left')
            if ke.keysym == 'Right':
                opQueue.put('Right')
            if ke.keysym == 'Up':
                opQueue.put('Up')
            if ke.keysym == 'Down':
                opQueue.put('Down')
            if ke.keysym == 'space':
                opQueue.put('space')


    def updateGameInfo(self, speed, levels, scores):
        self.speedVar.set(speed)
        self.levelsVar.set(levels)
        self.scoresVar.set(scores)
        print("update game infomation.")

    def setStartButtonText(self, text):
        self.btnStartVar.set(text)

    def btnStartClicked(self):
        if self.game.getGameRunningStatus() == 0:
            self.btnStartVar.set("Pause")
            self.game.start()
        elif self.game.getGameRunningStatus() == 1:
            self.btnStartVar.set("Resume")
            self.game.pause()
        elif self.game.getGameRunningStatus() == 5:
            self.btnStartVar.set("Pause")
            self.game.resume()


    def btnPlaybackClicked(self):
        print("playback ... ")
        self.gameCanvas.focus_set()


    def comboxClicked(self, event):
        print(self.cobox.get())
        print("combobox ... ")
        self.gameCanvas.focus_set()


    def rootClose(self, root):
        print("timer close.")
        if hasattr(self.game, "tick"):
            self.game.tick.cancel()
        opQueue.put("quit")
        time.sleep(0.3)
        root.quit()