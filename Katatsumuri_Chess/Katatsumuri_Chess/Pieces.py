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


WHITE = 'WHITE'
BLACK = 'BLACK'

class Base:
    def __init__(self):
        self.color = None
        self.attack_squares = []
        self.symbol = ['', '']

class Pawn(Base):
    def __init__(self, color):
        super().__init__()
        self.color = color
        if self.color == WHITE:
            self.attack_squares = ((-1, -1), (-1, 1))
        else:
            self.attack_squares = ((1, -1), (1, 1))
        self.symbol = ['P', 'p']

class Knight(Base):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.attack_squares = ((-2, -1), (-2, 1),
                                          (-1, 2),  (1, 2),
                                          (2, 1),    (2, -1),
                                          (1, -2),   (-1, -2))
        self.symbol = ['N', 'n']

class Bishop(Base):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.attack_squares = ((-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7),
                               (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7),
                               (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                               (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7))
        self.symbol = ['B', 'b']

class Rook(Base):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.attack_squares = ((-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0),
                               (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                               (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                               (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7))
        self.symbol = ['R', 'r']

class Queen(Base):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.attack_squares = ((-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7),
                               (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7),
                               (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                               (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7),
                               (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0),
                               (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                               (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                               (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7))
        self.symbol = ['Q', 'q']

class King(Base):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.attack_squares = ((-1, -1), (-1, 0), (-1, 1),
                               (0, -1), (0, 1),
                               (1, -1), (1, 0), (1, 1))
        self.symbol = ['K', 'k']

Pawn_type = type(Pawn('a'))
Knight_type = type(Knight('a'))
Bishop_type = type(Bishop('a'))
Rook_type = type(Rook('a'))
Queen_type = type(Queen('a'))
King_type = type(King('a'))
