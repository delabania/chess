import pygame
import sys

from view import BoardView

def handle_user_events(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            handle_click(position, game)

def handle_click(click, game):
    cell = BoardView.pixels_to_coordinates(*click)
    if game.is_current_user_piece_on_cell(cell):
        game.select_piece(cell)
    elif game.get_selected_piece():
        game.move_selected_piece(cell)

