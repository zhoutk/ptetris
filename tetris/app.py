# -*- coding: UTF-8 -*-
from tetris.game import Game
from tetris.tetris import Tetris
from tkinter import *
from tkinter import ttk
import tkinter
from tetris.block import *
import random

def start():
    root = Tk()
    root.title("Tetris")
    root.geometry('470x630')
    root.resizable(0, 0)
    App(root)
    root.mainloop()


class App:
    def __init__(self,root):
        self.gameCanvas = Canvas(root, bg='black', height=600 + CANVASOFFSET * 2, width=300 + CANVASOFFSET * 2)
        self.gameCanvas.place(x=12, y=10)

        self.next = Canvas(root, bg='black', height=120 + CANVASOFFSET * 2, width=120 + CANVASOFFSET * 2)
        self.next.place(x = 330, y = 10)

        frame = Frame(root)
        frame.place(x = 330, y = 160)

        Label(frame, text = "SPEED:").pack(anchor="w")
        self.speed = Label(frame, height=1, width=12, relief=SUNKEN, bd=1)
        self.speed.pack(anchor="w")

        Label(frame, text = "LEVELS:").pack(anchor="w")
        self.levels = Label(frame, height=1, width=12, relief=SUNKEN, bd=1)
        self.levels.pack(anchor="w")

        Label(frame, text = "SCORES:").pack(anchor="w")
        self.scores = Label(frame, height=1, width=12, relief=SUNKEN, bd=1)
        self.scores.pack(anchor="w")

        Label(frame, text = "").pack(anchor="w")
        Checkbutton(frame, text = "AutoPlay").pack(anchor="w")
        Button(frame, text = "Start", height=1, width=10, command=self.btnStartClicked).pack(anchor="w")

        Label(frame, text = "").pack(anchor="w")
        coboxVar = tkinter.StringVar
        cobox = ttk.Combobox(frame, textvariable=coboxVar, height=5, width=8, state="readonly")
        cobox.pack(anchor="w")
        cobox["value"] = ("last", "one", "two", "three")
        cobox.current(0)
        cobox.bind("<<ComboboxSelected>>", self.comboxClicked)
        self.cobox = cobox
        Button(frame, text = "PlayBack", height=1, width=10, command = self.btnPlaybackClicked).pack(anchor="w")

        self.gameCanvas.bind(sequence="<Key>", func=self.processKeyboardEvent)
        self.gameCanvas.focus_set()


    def processKeyboardEvent(self, ke):
        if ke.keysym == 'Left':
            self.t.moveLeft()
        if ke.keysym == 'Right':
            self.t.moveRight()
        if ke.keysym == 'Up':
            self.t.rotate()
        if ke.keysym == 'Down':
            self.t.moveDown()


    def btnStartClicked(self):
        if hasattr(self, 't'):
            self.t.clean()
        shape = random.randint(0,6)
        self.t = Tetris(self.gameCanvas, 1, 1, shape, "red")
        print("start ... ", shape)
        self.game = Game(self.gameCanvas)
        self.gameCanvas.focus_set()


    def btnPlaybackClicked(self):
        print("playback ... ")
        self.gameCanvas.focus_set()


    def comboxClicked(self, event):
        print(self.cobox.get())
        print("combobox ... ")
        self.gameCanvas.focus_set()