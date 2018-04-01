#colors

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 472, 472

CELL_SIZE = 59
PIECE_SIZE = 45
IMAGE_OFFSET = (CELL_SIZE - PIECE_SIZE) / 2


FPS = 50

PIECES = {
    'king': [4], 'queen': [3],
    'rook': [0, 7], 'knight': [1, 6], 'bishop': [2, 5] 
}
PAWN_COUNT = 8
