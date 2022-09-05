"""
This file is part of Katatsumuri_Chess

Copyright (c) 2022 YuaHyodo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .Pieces import*

WHITE = 'WHITE'
BLACK = 'BLACK'

class Board:
    def __init__(self, fen=None):
        self.fen_to_piece_class = {'P': Pawn, 'N': Knight, 'B': Bishop, 'R': Rook, 'Q': Queen, 'K': King}
        self.fen_white_to_black = {'P': 'p', 'N': 'n', 'B': 'b', 'R': 'r', 'Q': 'q', 'K': 'k'}
        self.fen_black_to_white = {b: w for w, b in self.fen_white_to_black.items()}

        self.castling_moves = {WHITE: {'e1g1': 0, 'e1c1': 1}, BLACK: {'e8g8': 0, 'e8c8': 1}}
        self.turn_dict = {WHITE: BLACK, BLACK: WHITE}
        
        self.init_board()
        if fen == None:
            self.set_startpos()
        else:
            self.set_fen(fen)

    def __str__(self):
        output = ''
        for i in range(8):
            rank = ''
            for j in range(8):
                sq = self.squares[i][j]
                if sq == None:
                    rank += '-'
                else:
                    if sq.color == WHITE:
                        index= 0
                    else:
                        index = 1
                    rank += sq.symbol[index]
            output += rank
            if i != 7:
                output += '\n'
        return output

    def init_board(self):
        self.squares = []
        for i in range(8):
            rank = []
            for j in range(8):
                rank.append(None)
            self.squares.append(rank)
        self.CastlingAbility = {WHITE: [True, True], BLACK: [True, True]}
        self.move_count = [0, 0]
        self.enpassant_square = None
        self.turn_of = None
        self.fen_list = []
        return

    def set_startpos(self):
        self.set_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        return

    def set_fen(self, fen):
        self.init_board()
        if len(self.fen_list) == 0:
            self.fen_list = [fen]
        fen = fen.split(' ')

        pieces = ''.join(fen[0].split('/'))
        numbers = [str(i) for i in range(10)]
        index = 0
        for i in range(len(pieces)):
            piece = pieces[i]
            if piece in numbers:
                index += int(piece)
                continue
            if piece in self.fen_black_to_white.keys():
                piece = self.fen_black_to_white[piece]
                self.squares[index // 8][index % 8] = self.fen_to_piece_class[piece](BLACK)
            else:
                self.squares[index // 8][index % 8] = self.fen_to_piece_class[piece](WHITE)
            index += 1

        if fen[1] == 'w':
            self.turn_of = WHITE
        else:
            self.turn_of = BLACK

        if fen[2] == '-':
            self.CastlingAbility = {WHITE: [False, False], BLACK: [False, False]}
        else:
            self.CastlingAbility = {WHITE: [False, False], BLACK: [False, False]}
            if 'K' in fen[2]:
                self.CastlingAbility[WHITE][0] = True
            if 'Q' in fen[2]:
                self.CastlingAbility[WHITE][1] = True
            if 'k' in fen[2]:
                self.CastlingAbility[BLACK][0] = True
            if 'q' in fen[2]:
                self.CastlingAbility[BLACK][1] = True

        if fen[3] == '-':
            self.enpassant_square = None
        else:
            self.enpassant_square = fen[3]

        self.move_count = [int(fen[4]), int(fen[5])]
        return

    def return_fen(self):
        pieces = ''
        c = 0
        for i in range(8):
            for j in range(8):
                piece = self.squares[i][j]
                if piece == None:
                    c += 1
                else:
                    if c != 0:
                        pieces += str(c)
                    c = 0
                    if piece.color == WHITE:
                        pieces += piece.symbol[0]
                    else:
                        pieces += piece.symbol[1]
            if c != 0:
                pieces += str(c)
                c = 0
            if i != 7:
                pieces += '/'
        fen = pieces + ' '

        fen += {WHITE: 'w ', BLACK: 'b '}[self.turn_of]

        if (True not in self.CastlingAbility[WHITE]) and (True not in self.CastlingAbility[BLACK]):
            fen += '- '
        else:
            if self.CastlingAbility[WHITE][0]:
                fen += 'K'
            if self.CastlingAbility[WHITE][1]:
                fen += 'Q'
            if self.CastlingAbility[BLACK][0]:
                fen += 'k'
            if self.CastlingAbility[BLACK][1]:
                fen += 'q'
            fen += ' '

        if self.enpassant_square == None:
            fen += '- '
        else:
            fen += (self.enpassant_square + ' ')

        fen += (str(self.move_count[0]) + ' ' + str(self.move_count[1]))
        return fen

    def piece_count(self):
        output = [[0] * 6, [0] * 6]
        fen = self.return_fen()
        pieces = fen.split(' ')[0]
        symbols = [['P', 'N', 'B', 'R', 'Q', 'K'], ['p', 'n', 'b', 'r', 'q', 'k']]
        for i in range(len(symbols[0])):
            output[0][i] = pieces.count(symbols[0][i])
        for i in range(len(symbols[1])):
            output[1][i] = pieces.count(symbols[1][i])
        return output

    def change_turn(self):
        self.turn_of = self.turn_dict[self.turn_of]
        return

    def index_to_uci(self, index):
        uci = ''
        d = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        uci += d[index[1]]
        uci += str(8 - index[0])
        return uci

    def uci_to_index(self, uci):
        d = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        index = [8 - int(uci[1]), d[uci[0]]]
        return index

    def move_from_uci(self, uci):
        move = {'from': [0, 0], 'to': [0, 0], '+': None}
        d = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        move['from'] = self.uci_to_index(uci[0:2])
        move['to'] = self.uci_to_index(uci[2:4])
        if len(uci) == 5:
            move['+'] = uci[4]
        return move

    def move_to_uci(self, move):
        uci = ''
        d = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        uci += self.index_to_uci(move['from'])
        uci += self.index_to_uci(move['to'])
        if move['+'] != None:
            uci += move['+']
        return uci

    def push_index(self, index_move):
        piece = self.squares[index_move['from'][0]][index_move['from'][1]]
        if self.squares[index_move['to'][0]][index_move['to'][1]] != None or type(piece) == Pawn_type:
            self.move_count[0] = 0
        else:
            self.move_count[0] += 1
        self.squares[index_move['to'][0]][index_move['to'][1]] = piece
        self.squares[index_move['from'][0]][index_move['from'][1]] = None
        self.enpassant_square = None
        if type(piece) == King_type:
            if self.turn_of == WHITE:
                self.CastlingAbility[WHITE] = [False, False]
            else:
                self.CastlingAbility[BLACK] = [False, False]
            uci_move = self.move_to_uci(index_move)
            if uci_move in self.castling_moves[self.turn_of].keys():
                if uci_move == 'e1g1':
                    piece = self.squares[7][7]
                    self.squares[7][7] = None
                    self.squares[7][5] = piece
                elif uci_move == 'e1c1':
                    piece = self.squares[7][0]
                    self.squares[7][0] = None
                    self.squares[7][3] = piece
                elif uci_move == 'e8g8':
                    piece = self.squares[0][7]
                    self.squares[0][7] = None
                    self.squares[0][5] = piece
                elif uci_move == 'e8c8':
                    piece = self.squares[0][0]
                    self.squares[0][0] = None
                    self.squares[0][3] = piece
        elif type(piece) == Rook_type:
            if index_move['from'][0] == 7 and index_move['from'][1] == 0:
                self.CastlingAbility[WHITE][1] = False
            if index_move['from'][0] == 7 and index_move['from'][1] == 7:
                self.CastlingAbility[WHITE][0] = False
            if index_move['from'][0] == 0 and index_move['from'][1] == 0:
                self.CastlingAbility[BLACK][1] = False
            if index_move['from'][0] == 0 and index_move['from'][1] == 7:
                self.CastlingAbility[BLACK][0] = False
        elif type(piece) == Pawn_type and abs(index_move['to'][0] - index_move['from'][0]) == 2:
            self.enpassant_square = self.index_to_uci(self.return_route(index_move)[0])
        elif type(piece) == Pawn_type and index_move['+'] != None:
            d = {'n': Knight, 'b': Bishop, 'r': Rook, 'q': Queen}
            self.squares[index_move['to'][0]][index_move['to'][1]] = d[index_move['+']](self.turn_of)

        if index_move['to'][0] == 0 and index_move['to'][1] == 0:
            self.CastlingAbility[BLACK][1] = False
        if index_move['to'][0] == 0 and index_move['to'][1] == 7:
            self.CastlingAbility[BLACK][0] = False
        if index_move['to'][0] == 7 and index_move['to'][1] == 0:
            self.CastlingAbility[WHITE][1] = False
        if index_move['to'][0] == 7 and index_move['to'][1] == 7:
            self.CastlingAbility[WHITE][0] = False
        
        if self.turn_of == BLACK:
            self.move_count[1] += 1
        self.change_turn()
        self.fen_list.append(self.return_fen())
        return

    def push(self, uci_move):
        index_move = self.move_from_uci(uci_move)
        self.push_index(index_move)
        return

    def pop(self):
        self.fen_list.pop(-1)
        self.set_fen(self.fen_list[-1])
        return

    def return_route(self, move):
        from_sq = move['from']
        to_sq = move['to']
        output = []
        if from_sq[0] == to_sq[0]:
            if from_sq[1] > to_sq[1]:
                for i in range(1, from_sq[1] - to_sq[1]):
                    output.append((to_sq[0], to_sq[1] + i))
            else:
                for i in range(1, to_sq[1] - from_sq[1]):
                    output.append((from_sq[0], from_sq[1] + i))
                    
        elif from_sq[1] == to_sq[1]:
            if from_sq[0] > to_sq[0]:
                for i in range(1, from_sq[0] - to_sq[0]):
                    output.append((to_sq[0] + i, to_sq[1]))
            else:
                for i in range(1, to_sq[0] - from_sq[0]):
                    output.append((from_sq[0] + i, from_sq[1]))
        
        else:
            if to_sq[0] > from_sq[0] and to_sq[1] > from_sq[1]:
                for i in range(1, to_sq[0] - from_sq[0]):
                    output.append((from_sq[0] + i, from_sq[1] + i))
                    
            elif to_sq[0] > from_sq[0] and to_sq[1] < from_sq[1]:
                for i in range(1, to_sq[0] - from_sq[0]):
                    output.append((from_sq[0] + i, from_sq[1] - i))
                    
            elif to_sq[0] < from_sq[0] and to_sq[1] > from_sq[1]:
                for i in range(1, from_sq[0] - to_sq[0]):
                    output.append((from_sq[0] - i, from_sq[1] + i))
            else:
                for i in range(1, from_sq[0] - to_sq[0]):
                    output.append((from_sq[0] - i, from_sq[1] - i))
        return output

    def is_legal_pseudo(self, move):
        #
        move_piece = self.squares[move['from'][0]][move['from'][1]]
        if move_piece == None:
            return False
        if move_piece.color != self.turn_of:
            return False
        #
        if min(move['to']) < 0 or max(move['to']) > 7:
            return False
        #
        sq = self.squares[move['to'][0]][move['to'][1]]
        if sq != None and sq.color == self.turn_of:
            return False
        #
        if move['+'] != None:
            if type(move_piece) != Pawn_type:
                return False
            if move_piece.color == WHITE and move['to'][0] != 0:
                return False
            if move_piece.color == BLACK and move['to'][0] != 7:
                return False
        #
        if type(move_piece) == Pawn_type:
            if self.turn_of == WHITE and move['to'][0] == 0 and move['+'] == None:
                return False
            if self.turn_of == BLACK and move['to'][0] == 7 and move['+'] == None:
                return False
            
            if move['from'][1] == move['to'][1]:
                if self.squares[move['to'][0]][move['to'][1]] != None:
                    return False
                if self.turn_of == WHITE:
                    start_rank = 6
                else:
                    start_rank = 1
                if move['from'][0] != start_rank and abs(move['from'][0] - move['to'][0]) != 1:
                    return False
                if self.turn_of == WHITE:
                    if move['from'][0] <= move['to'][0]:
                        return False
                else:
                    if move['from'][0] >= move['to'][0]:
                        return False
                if abs(move['from'][0] - move['to'][0]) == 2:
                    route_squares = self.return_route(move)
                    for route in route_squares:
                        if self.squares[route[0]][route[1]] != None:
                            return False
            else:
                for i in range(len(move_piece.attack_squares) + 1):
                    if i == len(move_piece.attack_squares):
                        return False
                    index = [move['from'][0] + move_piece.attack_squares[i][0],
                                 move['from'][1] + move_piece.attack_squares[i][1]]
                    if move['to'][0] == index[0] and move['to'][1] == index[1]:
                        break
                sq = self.squares[index[0]][index[1]]
                if self.index_to_uci(index) == self.enpassant_square:
                    pass
                elif sq == None or sq.color == self.turn_of:
                    return False
        else:
            for i in range(len(move_piece.attack_squares) + 1):
                if i == len(move_piece.attack_squares):
                    return False
                index = [move['from'][0] + move_piece.attack_squares[i][0],
                             move['from'][1] + move_piece.attack_squares[i][1]]
                if move['to'][0] == index[0] and move['to'][1] == index[1]:
                    break
            if type(move_piece) == Knight_type:
                pass
            else:
                route = self.return_route(move)
                for i in route:
                    sq = self.squares[i[0]][i[1]]
                    if sq != None:
                        return False
        return True

    def is_attackable(self, move):
        from_sq = move['from']
        to_sq = move['to']
        if max(to_sq) > 7 or min(to_sq) < 0:
            return False
        if type(self.squares[from_sq[0]][from_sq[1]]) == Knight_type:
            return True
        else:
            route_squares = self.return_route(move)
            for sq in route_squares:
                if self.squares[sq[0]][sq[1]] != None:#障害物あり
                    return False
        return True

    def return_attack_squares(self, turn):
        backup_turn_of = self.turn_of
        self.turn_of = turn
        moves = []
        for i in range(8):
            for j in range(8):
                sq = self.squares[i][j]
                if sq != None and sq.color == self.turn_of:
                    for k in range(len(sq.attack_squares)):
                        index =  [i + sq.attack_squares[k][0],
                                       j + sq.attack_squares[k][1]]
                        move = {'from': [i, j], 'to': index, '+': None}
                        if index not in moves and self.is_attackable(move):
                            moves.append(move)
        attack_squares = []
        for move in moves:
            if move['to'] not in attack_squares:
                attack_squares.append(move['to'])
        self.turn_of = backup_turn_of
        return attack_squares

    def is_legal_castling(self, move, index):
        if not self.CastlingAbility[self.turn_of][index]:
            return False
        if self.is_check():
            return False
        route_move_dict = {'e8g8': 'e8h8', 'e8c8': 'e8a8', 'e1g1': 'e1h1', 'e1c1': 'e1a1'}
        route_move_dict2 = {'e8g8': 'e8h8', 'e8c8': 'e8b8', 'e1g1': 'e1h1', 'e1c1': 'e1b1'}
        
        move1 = route_move_dict[self.move_to_uci(move)]
        move1 = self.move_from_uci(move1)
        
        move2 = route_move_dict2[self.move_to_uci(move)]
        move2 = self.move_from_uci(move2)
        
        route = self.return_route(move1)
        route2 = self.return_route(move2)
        
        attacked_squares = self.return_attack_squares(self.turn_dict[self.turn_of])
        for i in range(len(route)):
            sq = self.squares[route[i][0]][route[i][1]]
            if sq != None:
                return False
        for i in range(len(route2)):
            for j in range(len(attacked_squares)):
                if route2[i][0] == attacked_squares[j][0] and route2[i][1] == attacked_squares[j][1]:
                    return False
        return True

    def is_legal(self, uci_move):
        move = self.move_from_uci(uci_move)
        if type(self.squares[move['from'][0]][move['from'][1]]) == King_type:
            if uci_move in self.castling_moves[self.turn_of].keys():
                sq = self.squares[move['from'][0]][move['from'][1]]
                if type(sq) != King_type or sq.color != self.turn_of:
                    return False
                return self.is_legal_castling(move, self.castling_moves[self.turn_of][uci_move])
        if not self.is_legal_pseudo(move):
            return False
        if self.is_suiside_move(move):
            return False
        return True

    def is_check(self):
        attack_squares = self.return_attack_squares(self.turn_dict[self.turn_of])
        for i in attack_squares:
            sq = self.squares[i[0]][i[1]]
            if type(sq) == King_type and sq.color == self.turn_of:
                return True
        return False

    def is_suiside_move(self, move):
        self.push_index(move)
        self.change_turn()
        if self.is_check():
            self.pop()
            return True
        self.pop()
        return False

    def legal_moves(self):
        candidate_moves = []
        for i in range(8):
            for j in range(8):
                sq = self.squares[i][j]
                if sq != None and sq.color == self.turn_of:
                    for k in range(len(sq.attack_squares)):
                        index = [i + sq.attack_squares[k][0],
                                     j + sq.attack_squares[k][1]]
                        if max(index) > 7 or min(index) < 0:
                            continue
                        candidate_moves.append({'from': [i, j], 'to': index, '+': None})
                        if index[0] in [0, 7]:
                            candidate_moves.append({'from': [i, j], 'to': index, '+': 'n'})
                            candidate_moves.append({'from': [i, j], 'to': index, '+': 'b'})
                            candidate_moves.append({'from': [i, j], 'to': index, '+': 'r'})
                            candidate_moves.append({'from': [i, j], 'to': index, '+': 'q'})
                    if type(sq) == Pawn_type:
                        move_squares = ((-2, 0), (-1, 0), (1, 0), (2, 0))
                        for k in range(4):
                            index = [i + move_squares[k][0],
                                          j + move_squares[k][1]]
                            if max(index) > 7 or min(index) < 0:
                                continue
                            candidate_moves.append({'from': [i, j], 'to': index, '+': None})
                            if index[0] in [0, 7]:
                                candidate_moves.append({'from': [i, j], 'to': index, '+': 'n'})
                                candidate_moves.append({'from': [i, j], 'to': index, '+': 'b'})
                                candidate_moves.append({'from': [i, j], 'to': index, '+': 'r'})
                                candidate_moves.append({'from': [i, j], 'to': index, '+': 'q'})
        candidate_moves.extend([self.move_from_uci(move) for move in self.castling_moves[WHITE].keys()])
        candidate_moves.extend([self.move_from_uci(move) for move in self.castling_moves[BLACK].keys()])
        legal_moves = []
        for move in candidate_moves:
            move = self.move_to_uci(move)
            if move not in legal_moves and self.is_legal(move):
                legal_moves.append(move)
        return legal_moves

    def is_stalemate(self):
        if self.is_check():
            return False
        return len(self.legal_moves()) == 0

    def is_checkmate(self):
        return self.is_check() and len(self.legal_moves()) == 0

    def is_insufficient_material(self):
        pieces = self.piece_count()
        if max(pieces[0][0:5]) != 0 and max(pieces[1][0:5]) != 0:
            return False
        if pieces[0][0] >= 1 or pieces[1][0] >= 1:#P
            return False
        if pieces[0][3] >= 1 or pieces[1][3] >= 1:#R
            return False
        if pieces[0][4] >= 1 or pieces[1][4] >= 1:#Q
            return False
        if pieces[0][1] >= 2 or pieces[1][1] >= 2:#BB
            return False
        if pieces[0][1] == 1 and pieces[0][2] == 1:#BN
            return False
        if pieces[1][1] == 1 and pieces[1][2] == 1:#BN
            return False
        return True

    def is_draw(self):
        return self.is_insufficient_material() or self.is_stalemate() or self.move_count[0] >= 100


