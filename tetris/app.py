# -*- coding: UTF-8 -*-
from tetris.tetris import Tetris
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
        self.game = Canvas(root, bg='black', height=600, width=300)
        self.game.place(x=12, y=10)

        self.next = Canvas(root, bg='black', height=120, width=120)
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

        self.game.bind(sequence="<Key>", func=self.processKeyboardEvent)
        self.game.focus_set()


    def processKeyboardEvent(self, ke):
        if ke.keysym == 'Left':
            self.t.moveLeft()
        if ke.keysym == 'Right':
            self.t.moveRight()
        if ke.keysym == 'Up':
            self.t.moveUp()
        if ke.keysym == 'Down':
            self.t.moveDown()


    def btnStartClicked(self):
        if hasattr(self, 't'):
            self.t.clean()
        self.t = Tetris(self.game, 1, 1, 0, "white")
        print("start ... ")


    def btnPlaybackClicked(self):
        print("playback ... ")


    def comboxClicked(self, event):
        print(self.cobox.get())
        print("combobox ... ")
        self.game.focus_set()