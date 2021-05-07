'''
Created on May 5, 2021

@author: garycalvin
'''
COLUMNS = 'abcdefgh'
ROWS = '12345678'
PIECES = {'P': 1, 'R': 2, 'N': 3, 'B': 4, 'Q': 5, 'K': 6}
STARTING_POS = [2, 3, 4, 5, 6, 4, 3, 2,
                1, 1, 1, 1, 1, 1, 1, 1,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                -1, -1, -1, -1, -1, -1, -1, -1,
                -2, -3, -4, -5, -6, -4, -3, -2]

en_passant_square = None


def column_num(col):
    assert len(col) == 1
    assert col >= 'a' and col <= 'h'
    return ord(col) - ord('a')


def row_num(row):
    assert len(row) == 1
    assert row >= '1' and row <= '8'
    return ord(row) - ord('1')


def algebraic_to_index(alg):
    assert len(alg) == 2
    return row_num(alg[1]) * 8 + column_num(alg[0])


def index_to_algebraic(num):
    assert int == type(num)
    assert num >= 0 and num <= 63
    col = COLUMNS[num % 8]
    row = ROWS[num // 8]
    return col + row


def piece_alpha(num):
    num = abs(num)
    assert num in PIECES.values()
    for key, value in PIECES.items():
        if value == num:
            result = key
            break
    return result


def piece_num(alpha, color='white'):
    assert len(alpha) == 1
    assert alpha in PIECES.keys()
    sign = 1 if color == 'white' else -1
    return sign * PIECES[alpha]


def sign(num):
    return 0 if num == 0 else -1 if num < 0 else 1


def rank_distance(src, dest):
    if str == type(src):
        src = algebraic_to_index(src)
    if str == type(dest):
        dest = algebraic_to_index(dest)

    assert src >= 0 and src <= 63
    assert dest >= 0 and dest <= 63

    return abs(dest // 8 - src // 8)


def file_distance(src, dest):
    if str == type(src):
        src = algebraic_to_index(src)
    if str == type(dest):
        dest = algebraic_to_index(dest)

    assert src >= 0 and src <= 63
    assert dest >= 0 and dest <= 63

    return abs(dest % 8 - src % 8)


def locate_pieces(position, piece, color='white'):
    if str == type(piece):
        piece = piece_num(piece)
    sign = 1 if color == 'white' else -1
    piece = sign * piece
    result = []
    for i in range(len(position)):
        if position[i] == piece:
            result.append(i)

    return result


def get_direction(src, dest):
    if str == type(src):
        src = algebraic_to_index(src)
    if str == type(dest):
        dest = algebraic_to_index(dest)
    assert src >= 0 and src <= 63
    assert dest >= 0 and dest <= 63
    assert src != dest

    return sign(dest // 8 - src // 8) * 8 + sign(dest % 8 - src % 8)


def pawn_move_can_reach(position, src, dest):
    if str == type(src):
        src = algebraic_to_index(src)
    if str == type(dest):
        dest = algebraic_to_index(dest)
    assert src >= 0 and src <= 63
    assert dest >= 0 and dest <= 63
    assert src != dest
    my_sign = sign(position[src])

    if dest - src == my_sign * 8:
        if position[dest] == 0:
            return True

    if dest - src == my_sign * 16 and position[dest] == 0:
        # make sure we're on a starting square
        if position[src] == STARTING_POS[src]:
            if position[src + my_sign * 8] == 0:
                return True

    if dest - src == my_sign * 7 \
            and dest % 8 - src % 8 == dest // 8 - src // 8 \
            and sign(position[dest]) != my_sign:
        return True

    if dest - src == my_sign * 9 \
            and dest % 8 - src % 8 == dest // 8 - src // 8 \
            and sign(position[dest]) != my_sign:
        return True

    return False


def rook_move_can_reach(position, src, dest):
    if str == type(src):
        src = algebraic_to_index(src)
    if str == type(dest):
        dest = algebraic_to_index(dest)
    assert src >= 0 and src <= 63
    assert dest >= 0 and dest <= 63
    assert src != dest

    if 0 == rank_distance(src, dest) or 0 == file_distance(src, dest):
        d = get_direction(src, dest)
        nxt = src + d
        while nxt != dest:
            if position[nxt] != 0:
                return False
            nxt += d
        return True

    return False


def knight_move_can_reach(position, src, dest):
    if str == type(src):
        src = algebraic_to_index(src)
    if str == type(dest):
        dest = algebraic_to_index(dest)
    assert src >= 0 and src <= 63
    assert dest >= 0 and dest <= 63
    assert src != dest

    if abs(dest - src) in [6, 10, 15, 17]:
        if rank_distance(src, dest) + file_distance(src, dest) == 3:
            if sign(position[dest]) != sign(position[src]):
                return True

    return False


def bishop_move_can_reach(position, src, dest):
    if str == type(src):
        src = algebraic_to_index(src)
    if str == type(dest):
        dest = algebraic_to_index(dest)
    assert src >= 0 and src <= 63
    assert dest >= 0 and dest <= 63
    assert src != dest

    if rank_distance(src, dest) == file_distance(src, dest):
        if sign(position[src]) != sign(position[dest]):
            d = get_direction(src, dest)
            nxt = src + d
            while nxt != dest:
                if position[nxt] != 0:
                    return False
                nxt += d
            return True

    return False


def queen_move_can_reach(position, src, dest):
    return rook_move_can_reach(position, src, dest) \
        or bishop_move_can_reach(position, src, dest)


def king_move_can_reach(position, src, dest):
    if str == type(src):
        src = algebraic_to_index(src)
    if str == type(dest):
        dest = algebraic_to_index(dest)
    assert src >= 0 and src <= 63
    assert dest >= 0 and dest <= 63
    assert src != dest

    if 1 == rank_distance(src, dest) or 1 == file_distance(src, dest):
        return True

    return False


def can_reach(position, src, dest, piece=None):
    if str == type(src):
        src = algebraic_to_index(src)
    if str == type(dest):
        dest = algebraic_to_index(dest)
    assert src >= 0 and src <= 63
    assert dest >= 0 and dest <= 63
    assert src != dest

    if piece is None:
        piece = position[src]
    elif str == type(piece):
        piece = sign(position[src]) * piece_num(piece)
    func = [None, pawn_move_can_reach, rook_move_can_reach,
            knight_move_can_reach, bishop_move_can_reach,
            queen_move_can_reach, king_move_can_reach][abs(piece)]
    return func(position, src, dest)


def execute_move(position, src, dest, promote_to=None):
    global en_passant_square

    if str == type(src):
        src = algebraic_to_index(src)
    if str == type(dest):
        dest = algebraic_to_index(dest)
    assert src >= 0 and src <= 63
    assert dest >= 0 and dest <= 63
    assert src != dest

    new_position = position.copy()
    new_position[dest] = position[src]
    new_position[src] = 0

    if en_passant_square is not None and dest == en_passant_square:
        my_sign = sign(position[src])
        assert position[dest - my_sign * 8] == -my_sign  # enemy pawn
        new_position[dest - my_sign * 8] = 0

    if abs(position[src]) == 1:
        if abs(dest - src) == 16:
            en_passant_square = src + sign(position[src]) * 8
        else:
            en_passant_square = None
    else:
        en_passant_square = None

    return new_position


def get_destination(move_str):
    if move_str[:3] == 'O-O':
        return None


class Move(object):

    def parse_str(self, move_str, color):
        self.color = color
        self.sign = -1 if color == 'black' else 1

        if '+' in move_str:
            self.check = True
            move_str = move_str.replace('+', '')

        if '#' in move_str:
            self.checkmate = True
            move_str = move_str.replace('#', '')

        if move_str == 'O-O-O':
            self.castle = 'Q'
            return

        if move_str == 'O-O':
            self.castle = 'K'
            return

        if 'x' in move_str:
            self.capture = True
            move_str = move_str.replace('x', '')

        if '=' in move_str:
            eq = move_str.index('=')
            self.promote_to = move_str[eq + 1:eq + 2]
            move_str = move_str[:eq]

        dest = move_str[-2:]
        self.dest = algebraic_to_index(dest)
        move_str = move_str[:-2]

        if move_str == '':
            self.piece = 'P'
        elif move_str[0] in PIECES.keys():
            self.piece = move_str[0]
            move_str = move_str[1:]
        self.piece_val = self.sign * PIECES[self.piece]

        if move_str != '':
            if move_str[0] in 'abcdefgh':
                self.column = column_num(move_str[0])
                move_str = move_str[1:]
            elif move_str[0] in '12345678':
                self.row = row_num(move_str[0])
                move_str = move_str[1:]

    def __init__(self, position=STARTING_POS, move_str=None, color='white'):
        self.position = STARTING_POS
        self.color = 'white'
        self.sign = 1
        self.castle = None
        self.check = False
        self.checkmate = False
        self.capture = False
        self.promote_to = None
        self.row = None
        self.column = None
        self.piece = None
        self.piece_val = None
        self.src = None
        self.dest = None

        if move_str is not None:
            self.parse_str(move_str, color)
