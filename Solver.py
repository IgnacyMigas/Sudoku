import Board
import abc
import numpy


class AbstractSolver(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def solve(self):
        pass


class Solver(AbstractSolver):
    def __init__(self, board=Board.Board()):
        self.board = board
        self.solveBoard = numpy.zeros((9, 9), int)
        for i in range(9):
            for j in range(9):
                self.solveBoard[i][j] = self.board.get_board()[i][j]

    def solve(self):
        if self._solve(0, 0):
            self.board.set_board(self.solveBoard)
            return True
        return False

    def _can_insert(self, x, y, value):
        for i in range(9):
            if self.solveBoard[x][i] == value or self.solveBoard[i][y] == value or self.solveBoard[int(x/3)*3+i%3][int(y/3)*3+int(i/3)] == value:
                return False
        return True

    def _next(self, x, y):
        if x == 8 and y == 8:
            return True
        elif x == 8:
            return self._solve(0, y+1)
        else:
            return self._solve(x+1, y)

    def _solve(self, x, y):
        if self.board.get_board()[x][y] == 0:
            for i in range(1, 10):
                if self._can_insert(x, y, i):
                    self.solveBoard[x][y] = i
                    if self._next(x, y):
                        return True
            self.solveBoard[x][y] = 0
            return False
        return self._next(x, y)

    def printSolve(self):
        print "\nSolve: "
        for row in self.solveBoard:
            print ", ".join(map(str, row))

if __name__ == "__main__":
    board = Board.Board()
    print board.put(0, 0, 8)
    print board.put(0, 7, 1)
    print board.put(1, 1, 5)
    print board.put(1, 6, 9)
    print board.put(2, 2, 9)
    print board.put(2, 4, 2)
    print board.put(2, 7, 5)
    print board.put(2, 8, 6)
    print board.put(3, 1, 7)
    print board.put(3, 2, 8)
    print board.put(3, 3, 2)
    print board.put(3, 5, 9)
    print board.put(3, 6, 3)
    print board.put(4, 2, 5)
    print board.put(4, 3, 4)
    print board.put(4, 4, 6)
    print board.put(4, 5, 3)
    print board.put(4, 6, 1)
    print board.put(5, 2, 4)
    print board.put(5, 3, 7)
    print board.put(5, 5, 5)
    print board.put(5, 6, 6)
    print board.put(5, 7, 2)
    print board.put(6, 0, 5)
    print board.put(6, 1, 8)
    print board.put(6, 4, 3)
    print board.put(6, 6, 2)
    print board.put(7, 2, 7)
    print board.put(7, 7, 9)
    print board.put(8, 1, 6)
    print board.put(8, 8, 7)
    solver = Solver(board)
    print board.get_board()
    print "solver:"
    solver.solve()
    print
    print solver.board.get_board()