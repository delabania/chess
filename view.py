import pygame
import sys

from constants import (
    WIDTH, HEIGHT, CELL_SIZE, WHITE, IMAGE_OFFSET, RED
)

def app_init():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('chess game')
    return screen

class BoardView():
    def __init__(self, screen, chessboard_image):
        self.chessboard_image = pygame.image.load(chessboard_image)
        self.pieces =  pygame.sprite.Group()
        self.screen = screen

    def update_chessboard(self, game):
        """
        <chessboard> is a current state of game object
        we have to translate abstract data {pawn : (1,1), ...}
        to explicit e.g. {'pawn.img': Rect(124, 124, 45, 45)}
        """
        self.pieces =  pygame.sprite.Group()
        self.selected_cell = None
        selected_piece = game.get_selected_piece()
        if selected_piece:
            self.selected_cell = BoardView.coordinates_to_pixels(
                *selected_piece.get_coordinates()
            )
        for piece in game.get_pieces():
            x, y = BoardView.coordinates_to_pixels(
                *piece.get_coordinates(), image=True
            )
            self.pieces.add(
                PieceView(piece.get_type(), piece.get_color(), x, y)
            )

    def highlight_cell(self, cell, color):
        cell_rect = pygame.Rect(cell, (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, color, cell_rect, 5)

    def draw(self):
        self.pieces.draw(self.screen)
        if self.selected_cell:
            self.highlight_cell(self.selected_cell, RED)

    @classmethod
    def coordinates_to_pixels(cls, x, y, image=False):
        if not image:
            return x * CELL_SIZE, y * CELL_SIZE
        return x * CELL_SIZE + IMAGE_OFFSET, y * CELL_SIZE + IMAGE_OFFSET 

    @classmethod
    def pixels_to_coordinates(self, x, y):
        return x // CELL_SIZE, y // CELL_SIZE

    def update_screen(self, game):
        self.update_chessboard(game)
        self.screen.fill(WHITE)
        self.screen.blit(self.chessboard_image, (0, 0))
        self.draw()
        pygame.display.flip()

class PieceView(pygame.sprite.Sprite):
    def __init__(self, type_, color, x, y):
        # x, y are pixel coordinates
        super(PieceView, self).__init__()
        image_filepath = 'static/{}_{}.png'.format(type_, color)
        self.image = pygame.image.load(image_filepath)
        self.rect = self.image.get_rect().move(x, y)