'''
Created on May 5, 2021

@author: garycalvin
'''
import unittest
import chess as ch

STARTING_POS = [2, 3, 4, 5, 6, 4, 3, 2,
                1, 1, 1, 1, 1, 1, 1, 1,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                -1, -1, -1, -1, -1, -1, -1, -1,
                -2, -3, -4, -5, -6, -4, -3, -2]


POS1 = [0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0]

POS2 = [0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 2, 6, 0, 1,
        1, 0, 0, -2, 0, 1, 0, -1,
        0, 0, 0, 0, 0, -1, 1, 0,
        0, -1, 0, 0, 1, 0, -6, 0,
        -1, 0, 0, 0, 0, -1, -1, 0,
        0, 0, 0, 0, 0, 0, 0, 0]

POS3 = [2, 0, 0, 0, 0, 2, 6, 0,
        1, 4, 1, 0, 0, 3, 1, 1,
        -1, 0, 0, 1, 0, 5, 0, 3,
        0, -1, 0, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, -1, 0, 4,
        0, 0, -3, 0, -1, 0, 0, -1,
        0, -1, 0, -3, -4, 0, -1, 0,
        -2, 0, -4, -5, 0, -2, -6, 0]


class Test(unittest.TestCase):

    def test_column_num(self):
        result = ch.column_num('a')
        assert result == 0
        result = ch.column_num('h')
        assert result == 7

    def test_row_num(self):
        result = ch.row_num('1')
        assert result == 0
        result = ch.row_num('8')
        assert result == 7

    def test_algebraic_to_index(self):
        result = ch.algebraic_to_index('a1')
        assert result == 0
        result = ch.algebraic_to_index('h8')
        assert result == 63

    def test_index_to_algebraic(self):
        result = ch.index_to_algebraic(0)
        assert result == 'a1'

    def test_piece_alpha(self):
        result = ch.piece_alpha(1)
        assert result == 'P'
        result = ch.piece_alpha(6)
        assert result == 'K'
        result = ch.piece_alpha(-5)
        assert result == 'Q'

    def test_piece_num(self):
        result = ch.piece_num('Q')
        assert result == 5
        result = ch.piece_num('B', 'black')
        assert result == -4

    def test_sign(self):
        result = ch.sign(-123)
        assert result == -1
        result = ch.sign(0)
        assert result == 0
        result = ch.sign(12345)
        assert result == 1

    def test_rank_distance(self):
        result = ch.rank_distance(0, 63)
        assert result == 7
        result = ch.rank_distance('a3', 'd5')
        assert result == 2

    def test_file_distance(self):
        result = ch.file_distance(0, 63)
        assert result == 7
        result = ch.file_distance('a3', 'd5')
        assert result == 3

    def test_locate_pieces(self):
        result = ch.locate_pieces(POS1, 1)
        assert result == []
        result = ch.locate_pieces(POS2, 1)
        assert result == [17, 23, 24, 29, 38, 44]
        result = ch.locate_pieces(POS2, 'K')
        assert result == [21]
        result = ch.locate_pieces(POS2, 'K', 'black')
        assert result == [46]
        result = ch.locate_pieces(POS3, -3)
        assert result == [42, 51]

    def test_get_direction(self):
        result = ch.get_direction('c8', 'a6')
        assert result == -9
        result = ch.get_direction('b2', 'a3')
        assert result == 7
        result = ch.get_direction('d4', 'a4')
        assert result == -1

    def test_pawn_move_can_reach(self):
        result = ch.pawn_move_can_reach(STARTING_POS, 11, 19)
        assert result is True
        result = ch.pawn_move_can_reach(STARTING_POS, 'd2', 'd4')
        assert result is True
        result = ch.pawn_move_can_reach(STARTING_POS, 'd2', 'd5')
        assert result is False
        result = ch.pawn_move_can_reach(POS2, 'f5', 'f4')
        assert result is False
        result = ch.pawn_move_can_reach(POS2, 'f7', 'f6')
        assert result is True
        result = ch.pawn_move_can_reach(POS2, 'e6', 'f7')
        assert result is True

    def test_rook_move_can_reach(self):
        result = ch.rook_move_can_reach(POS2, 'd4', 'a4')
        assert result is True
        result = ch.rook_move_can_reach(POS2, 'd4', 'e3')
        assert result is False

    def test_knight_move_can_reach(self):
        result = ch.knight_move_can_reach(POS3, 'f2', 'e4')
        assert result is True
        result = ch.knight_move_can_reach(POS3, 'f2', 'd4')
        assert result is False
        result = ch.knight_move_can_reach(POS3, 23, 33)
        assert result is False
        result = ch.knight_move_can_reach(POS3, 23, 38)
        assert result is True

    def test_bishop_move_can_reach(self):
        result = ch.bishop_move_can_reach(POS3, 'c8', 'a6')
        assert result is False
        result = ch.bishop_move_can_reach(POS3, 'b2', 'g7')
        assert result is True
        result = ch.bishop_move_can_reach(POS3, 'b2', 'a3')
        assert result is True
        result = ch.bishop_move_can_reach(POS3, 47, 56)
        assert result is False

    def test_queen_move_can_reach(self):
        result = ch.queen_move_can_reach(POS3, 'f3', 'c6')
        assert result is True
        result = ch.queen_move_can_reach(POS3, 'd8', 'h4')
        assert result is False

    def test_king_move_can_reach(self):
        result = ch.king_move_can_reach(POS3, 'g8', 'h8')
        assert result is True

    def test_can_reach(self):
        result = ch.can_reach(POS3, 'g8', 'h8')
        assert result is True
        result = ch.can_reach(POS3, 'd8', 'h4')
        assert result is False
        result = ch.can_reach(POS3, 'f3', 'c6')
        assert result is True
        result = ch.can_reach(POS3, 'f3', 'c6', 'R')
        assert result is False

    def test_execute_move(self):
        position = POS3.copy()
        assert position[21] == 5
        assert position[42] == -3
        new_position = ch.execute_move(position, 'f3', 'c6')
        assert new_position[21] == 0
        assert new_position[42] == 5
        position = STARTING_POS.copy()
        new_position = ch.execute_move(position, 'd2', 'd4')
        assert new_position[11] == 0
        assert new_position[27] == 1
        assert ch.en_passant_square == 19

    def test_move(self):
        move = ch.Move()
        assert move.position == ch.STARTING_POS
        assert move.color == 'white'
        assert move.dest is None
        move = ch.Move(STARTING_POS, 'e4', 'white')
        assert ch.Move == type(move)
        assert move.dest == 28
        assert move.piece == 'P'
        assert move.piece_val == 1
        move = ch.Move(STARTING_POS, 'c5', 'black')
        assert move.dest == 34
        assert move.piece == 'P'
        assert move.piece_val == -1


if __name__ == "__main__":
    unittest.main()
