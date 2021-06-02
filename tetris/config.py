import uuid

TETRISDIMENSION = 4
BLOCKSIDEWIDTH = 30
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
