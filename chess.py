from model import Game
from view import BoardView, app_init
from controller import handle_user_events

def main():
    screen  = app_init()
    board_view = BoardView(screen, 'static/chessboard.png')
    game = Game()
    
    while not game.end():
        handle_user_events(game)
        board_view.update_screen(game)

if __name__ == '__main__':
    main()

    