# -*- coding: UTF-8 -*-
from tetris.config import *

class Block(object):
    def __init__(self, object, x, y) -> None:
        self.pos = (x, y)
        object.create_rectangle((x - 1) * BLOCKSIDEWIDTH, (y - 1) * BLOCKSIDEWIDTH, x * BLOCKSIDEWIDTH, y * BLOCKSIDEWIDTH, fill = "blue")