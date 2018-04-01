from itertools import chain, izip
from constants import PIECES, PAWN_COUNT
from utils import get_range_between

class Game(object):
    def __init__(self):
        self.players = {
            'white': Player('user'),
            'black': Player('com')
        }
        self.init_chessboard()
        self.current_player_color = 'white'
        self.selected_piece = None

    def end(self):
        return self.is_mate()

    def is_mate(self):
        # mate (attack) on <color> king
        if self.is_check(self.current_player_color):
            #TODO: find whether there are possible moves
            possible_moves = True
            return not possible_moves
        return False

    def is_check(self, color):
        pieces = self.chessboard[color]
        king = filter(lambda piece: piece.type == 'king', pieces)[0]
        for piece in self.chessboard[self.get_next_player_color()]:
            if piece.check_move_is_allowed(self, *king.get_coordinates()):
                print 'check on {} king by {}'.format(self.current_player_color, piece)
                return True
        return False

    def get_next_player_color(self):
        if self.current_player_color == 'white':
            return 'black'
        return 'white'

    def init_chessboard(self):
        self.chessboard = {
            'white': self.locate_pieces('white'),
            'black': self.locate_pieces('black')
        }

    def get_selected_piece(self):
        return self.selected_piece

    def move_selected_piece(self, cell):
        other_piece = self.get_piece_on_cell(cell)
        if other_piece:
            other_piece_color = other_piece.get_color()
            if self.current_player_color == other_piece_color:
                return
        if not self.selected_piece.move(self, *cell):
            return
        self.selected_piece = None

        if other_piece:
            self.chessboard[other_piece_color].remove(other_piece)
            del other_piece

        self.current_player_color = self.get_next_player_color() 

    def locate_pieces(self, color):
        if color == 'black':
            piece_y = 0
            pawn_y = 1
        elif color == 'white':
            piece_y = 7
            pawn_y = 6

        pieces = []

        for piece, x_list in PIECES.iteritems():
            for x in x_list:
                pieces.append(Piece(piece, color, x, piece_y))
        for x in range(PAWN_COUNT):
            pieces.append(Piece('pawn', color, x, pawn_y))

        return pieces

    def get_pieces(self):
        return chain(self.chessboard['white'], self.chessboard['black'])

    def get_piece_on_cell(self, cell):
        # e.g cell = (1,2)
        for piece in self.get_pieces():
            if cell == piece.get_coordinates():
                return piece
        return None

    def select_piece(self, cell):
        piece = self.get_piece_on_cell(cell)
        if piece and piece.get_color() == self.current_player_color:
            self.selected_piece = piece

    def is_current_user_piece_on_cell(self, cell):
        piece = self.get_piece_on_cell(cell)
        if piece and piece.get_color() == self.current_player_color:
            return True
        return False

    def is_opponent_piece_on_cell(self, cell):
        piece = self.get_piece_on_cell(cell)
        if piece and piece.get_color() == self.get_next_player_color():
            return True
        return False

    def is_piece_on_way(self, start_x, start_y, finish_x, finish_y):
        """
        Checks are there any piece on way from start_cell to finish_cell.
        Watch out for pawn capturing in fly, castling, and knight movement.
        """
        x_diff = start_x - finish_x
        y_diff = start_y - finish_y
        # we do not count start nor finish cell
        way_length = max(abs(x_diff), abs(y_diff)) - 1
        x_range = get_range_between(start_x, finish_x, way_length)
        y_range = get_range_between(start_y, finish_y, way_length)
        cells = set(izip(x_range, y_range))
        pieces_positions = {
            piece.get_coordinates() for piece in self.get_pieces()
        }
        if cells.intersection(pieces_positions):
            return True
        return False


class Player(object):
    def __init__(self, who):
        self.who = who

class Piece(object):
    def __init__(self, type_, color, x, y):
        self.type = type_
        self.color = color
        self.x = x
        self.y = y
        self.in_initial_position = True # for pawns and kings

    def get_coordinates(self):
        return self.x, self.y

    def get_color(self):
        return self.color

    def get_type(self):
        return self.type

    def check_move_is_allowed(self, board, x, y):
        x_diff = x - self.x
        y_diff = y - self.y
        if self.type == 'rook':
            return (x_diff == 0 or y_diff == 0) and not board.is_piece_on_way(self.x, self.y, x, y)
        elif self.type == 'bishop':
            return abs(x_diff) == abs(y_diff) and not board.is_piece_on_way(self.x, self.y, x, y)
        elif self.type == 'knight':
            return abs(x_diff) ** 2 + abs(y_diff) ** 2 == 5
        elif self.type == 'queen':
            rook_move = (x_diff == 0 or y_diff == 0)
            bishop_move = abs(x_diff) == abs(y_diff)
            return (rook_move or bishop_move) and not board.is_piece_on_way(self.x, self.y, x, y)
        elif self.type == 'king':
            # normal king movement, castrling is checked earlier
            return abs(x_diff) <= 1 and abs(y_diff) <= 1
        elif self.type == 'pawn':
            if x_diff == 0:
                # normal movement
                if board.is_opponent_piece_on_cell((x, y)):
                    # we can capture opponent pieces only 
                    return False
                if self.color == 'black':
                    if self.in_initial_position:
                        return y_diff == 1 or y_diff == 2
                    return y_diff == 1
                else: # color == 'white'
                    if self.in_initial_position:
                        return y_diff == -1 or y_diff == -2
                    return y_diff == -1
            elif abs(x_diff) == 1:
                # normal capturing
                if not board.is_opponent_piece_on_cell((x, y)):
                    return False
                # could capture opponent piece
                if self.color == 'black':
                    return y_diff == 1
                else: # color == 'white'
                    return y_diff == -1
                # TODO: capturing on fly 
            
            # invalid movement
            return False

    def _check_castling_posibility(self, board, x, y):
        # self is king here!
        # TODO: check on king after castling - disable castling!
        assert self.type == 'king'
        x_diff = x - self.x
        y_diff = y - self.y
        if self.in_initial_position and y_diff == 0 and abs(x_diff) == 2:
            if not self._get_rook_in_castling(board, x_diff):
                return False
            # castling is possible iff the way is clear off other pieces
            return not board.is_piece_on_way(self.x, self.y, x, y)
        return False

    def _get_rook_in_castling(self, board, x_diff):
        if x_diff == 2:
            rook_pos = (7, self.y)
        else:
            rook_pos = (0, self.y)
        print 'king: ', self.x, self.y
        print x_diff
        print 'rook: ', rook_pos[0], rook_pos[1]
        piece = board.get_piece_on_cell(rook_pos)
        if not piece or piece.type != 'rook' or not piece.in_initial_position:
            return None
        return piece

    def _do_castling(self, board, x, y):
        x_diff = x - self.x
        rook = self._get_rook_in_castling(board, x_diff)
        self._move(x, y)
        if x_diff == -2:
            rook._move(x + 1, y)
        else:
            rook._move(x - 1, y)


    def move(self, board, x, y):
        if self.type == 'king' and self._check_castling_posibility(board, x, y):
            self._do_castling(board, x, y)
            return True
        if not self.check_move_is_allowed(board, x, y):
            return False
        self._move(x, y)
        return True

    def _move(self, x, y):
        self.x = x
        self.y = y
        self.in_initial_position = False


    def __str__(self):
        return '{} {}'.format(self.color, self.type)

