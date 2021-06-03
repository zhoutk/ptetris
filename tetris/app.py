# -*- coding: UTF-8 -*-
from tetris.game import Game
from tkinter import *
from tkinter import ttk
import tkinter
from tetris.block import *

def start():
    root = Tk()
    root.title("Tetris")
    root.geometry('470x630')
    root.resizable(0, 0)
    App(root)
    root.mainloop()


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
        self.speedVar = tkinter.StringVar()
        speed = Label(frame, height=1, width=12, relief=SUNKEN, bd=1, textvariable=self.speedVar)
        speed.pack(anchor="w")

        Label(frame, text = "LEVELS:").pack(anchor="w")
        self.levelsVar = tkinter.StringVar()
        levels = Label(frame, height=1, width=12, relief=SUNKEN, bd=1, textvariable=self.levelsVar)
        levels.pack(anchor="w")

        Label(frame, text = "SCORES:").pack(anchor="w")
        self.scoresVar = tkinter.StringVar()
        scores = Label(frame, height=1, width=12, relief=SUNKEN, bd=1, textvariable=self.scoresVar)
        scores.pack(anchor="w")

        Label(frame, text = "").pack(anchor="w")
        Checkbutton(frame, text = "AutoPlay").pack(anchor="w")
        Button(frame, text = "Start", height=1, width=10, command=self.btnStartClicked).pack(anchor="w")

        Label(frame, text = "").pack(anchor="w")
        coboxVar = tkinter.StringVar()
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
                self.game.moveLeft()
            if ke.keysym == 'Right':
                self.game.moveRight()
            if ke.keysym == 'Up':
                self.game.rotate()
            if ke.keysym == 'Down':
                self.game.moveDown()
            if ke.keysym == 'space':
                self.game.moveDownEnd()


    def updateGameInfo(self, speed, levels, scores):
        self.speedVar.set(speed)
        self.levelsVar.set(levels)
        self.scoresVar.set(scores)
        print("update game infomation.")


    def btnStartClicked(self):
        print("start ... ")
        self.game.start()


    def btnPlaybackClicked(self):
        print("playback ... ")
        self.gameCanvas.focus_set()


    def comboxClicked(self, event):
        print(self.cobox.get())
        print("combobox ... ")
        self.gameCanvas.focus_set()


    def rootClose(self, root):
        print("timer close.")
        self.game.tick.cancel()
        root.quit()