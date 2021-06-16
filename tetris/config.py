import uuid
from queue import Queue

opQueue = Queue()
WORKINTERVAL = 0.001
AUTOINTERVAL = 0
BACKINTERVAL = 0

TETRISDIMENSION = 4
BLOCKSIDEWIDTH = 30
HALFBLOCKWIDTH = BLOCKSIDEWIDTH // 2
CANVASOFFSET = 4
TETRISAHPES = (
    (1, 1, 1, 1),
    (0, 1, 1, 1, 0, 1),
    (1, 1, 1, 0, 0, 0, 1),
    (0, 1, 1, 0, 0, 1, 1),
    (1, 1, 0, 0, 0, 1, 1),
    (0, 1, 1, 0, 1, 1),
    (0, 1, 0, 0, 1, 1, 1)
)

TETRISCOLORS = (
    "red",
    "magenta",
    "darkMagenta",
    "gray",
    "darkGreen",
    "darkCyan",
    "darkBlue"
)

SCORES = (0,1,3,7,10)

STEPUPSCORE = 50
STEPUPINTERVAL = 100

GameRoom = [[0 for i in range(12)] for i in range(22)]

def initGameRoom():
    for i in range(22):
        for j in range(12):
            if i == 21 or j == 0 or j == 11: 
                GameRoom[i][j] = 1
            else:
                GameRoom[i][j] = 0

def UID():
    return str(uuid.uuid1()).split("-")[0]
