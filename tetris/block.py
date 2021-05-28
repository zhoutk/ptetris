# -*- coding: UTF-8 -*-
from tetris.config import *

class Block(object):
    def __init__(self, object, x, y) -> None:
        self.object = object
        self.x = x
        self.y = y
        self.obj = object.create_rectangle((x - 1) * BLOCKSIDEWIDTH, (y - 1) * BLOCKSIDEWIDTH, x * BLOCKSIDEWIDTH, y * BLOCKSIDEWIDTH, fill = "blue")


    def relocate(self, x, y):
        self.object.move(self.obj, (x - self.x) * BLOCKSIDEWIDTH, (y - self.y) * BLOCKSIDEWIDTH)
        self.x = x
        self.y = y