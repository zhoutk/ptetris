import uuid

TETRISDIMENSION = 4
BLOCKSIDEWIDTH = 30
CANVASOFFSET = 2
TETRISAHPES = (
    (1, 1, 1, 1),
    (0, 1, 1, 1, 0 , 1),
    (1, 1, 1, 0, 0, 0, 1),
    (0, 1, 1, 0, 0, 1, 1),
    (1, 1, 0, 0, 0, 1, 1),
    (0, 1, 1, 0, 1, 1),
    (0, 1, 0, 0, 1, 1, 1)
)

def UID():
    return str(uuid.uuid1()).split("-")[0]
