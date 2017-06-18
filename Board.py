#!/usr/bin/pyhon2.7.9

import abc


class AbstractBoard(object):
    __metaclass__ = abc.ABCMeta

    @abstractmethod
    def put(self, x, y, value):
        pass

    @abc.abstractmethod
    def get_board(self):
        pass

    @abc.abstractmethod
    def is_solved(self):
        pass


class Board(AbstractBoard):
    def __init__(self):
        self.board = [None]*9*9

    def put(self, x, y, value):
        if self._check_move_possible(x, y, value):
            self.board[x+y*9] = value
            return True
        return False

    def get_board(self):
        return self.board

    def is_solved(self):
        if None in self.board:
            return True
        return False

    def _check_move_possible(self, x, y, value):
        if self.board[x+y*9] is not None:
            return False
        for i in range(9):
            if self.board[x+i*9] == value or self.board[i+y*9] == value:
                return False
        xtmp = int(x/3)
        ytmp = int(y/3)
        print xtmp, ytmp
        for i in range(3):
            for j in range(3):
                if self.board[xtmp*3+i+(ytmp*3+j)*9] == value:
                    return False
        return True

if __name__ == "__main__":
    board = Board()
    print board.put(1, 1, 3)
    print board.put(1, 0, 4)
    print board.put(2, 5, 6)
    print board.put(0, 0, 3)
    print board.put(0, 1, 3)
    print board.put(0, 2, 3)
    print board.put(1, 0, 3)
    print board.put(1, 1, 3)
    print board.put(1, 2, 3)
    print board.put(2, 0, 3)
    print board.put(2, 1, 3)
    print board.put(2, 2, 3)
    if not board.is_solved():
        print board.get_board()
