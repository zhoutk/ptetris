# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import ttk
import tkinter

def start():
    root = Tk()
    root.title("Tetris")
    root.geometry('470x630')
    root.resizable(0, 0)
    App(root)
    root.mainloop()


class App(object):
    def __init__(self,object):
        game = Canvas(object, bg='black', height=600, width=300)
        game.place(x=15, y=10)

        next = Canvas(object, bg='black', height=120, width=120)
        next.place(x = 330, y = 10)

        frame = Frame(object)
        frame.place(x = 330, y = 160)

        Label(frame, text = "SPEED:").pack(anchor="w")
        self.speed = Label(frame, height=1, width=15, relief=SUNKEN, bd=1)
        self.speed.pack(anchor="w")

        Label(frame, text = "LEVELS:").pack(anchor="w")
        self.levels = Label(frame, height=1, width=15, relief=SUNKEN, bd=1)
        self.levels.pack(anchor="w")

        Label(frame, text = "SCORES:").pack(anchor="w")
        self.scores = Label(frame, height=1, width=15, relief=SUNKEN, bd=1)
        self.scores.pack(anchor="w")

        Label(frame, text = "").pack(anchor="w")
        Checkbutton(frame, text = "AutoPlay").pack(anchor="w")
        Button(frame, text = "Start", height=1, width=12).pack(anchor="w")

        Label(frame, text = "").pack(anchor="w")
        coboxVar = tkinter.StringVar
        cobox = ttk.Combobox(frame, textvariable=coboxVar, height=1, width=10, state="readonly")
        cobox.pack(anchor="w")
        cobox["value"] = ("last", "one", "two", "three")
        cobox.current(0)
        Button(frame, text = "PlayBack", height=1, width=12).pack(anchor="w")

        game.focus()