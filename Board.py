import abc
import numpy


class AbstractBoard(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def put(self, x, y, value):
        pass

    @abc.abstractmethod
    def get_board(self):
        pass

    @abc.abstractmethod
    def set_board(self, board):
        pass

    @abc.abstractmethod
    def is_solved(self):
        pass


class Board(AbstractBoard):
    def __init__(self):
        self.board = numpy.zeros((9, 9), int)

    def put(self, x, y, value):
        if self._check_move_possible(x, y, value):
            self.board[x][y] = value
            return True
        return False

    def get_board(self):
        return self.board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.board[i][j] = board[i][j]

    def is_solved(self):
        if 0 not in self.board:
            return True
        return False

    def _check_move_possible(self, x, y, value):
        if self.board[x][y] != 0:
            return False
        for i in range(9):
            if self.board[x][i] == value or self.board[i][y] == value or self.board[int(x/3)*3+i%3][int(y/3)*3+int(i/3)] == value:
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
    print board.get_board()

