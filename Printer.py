import pygame, sys, abc, numpy
import Board
from pygame.locals import *

#Number of frames per second
FPS = 10

# Sets size of grid
WINDOWMULTIPLIER = 7  # Modify this number to change size of grid
WINDOWSIZE = 90
WINDOWWIDTH = WINDOWSIZE * WINDOWMULTIPLIER
WINDOWHEIGHT = WINDOWSIZE * WINDOWMULTIPLIER
SQUARESIZE = (WINDOWSIZE * WINDOWMULTIPLIER) / 3  # size of a 3x3 square
CELLSIZE = SQUARESIZE / 3  # Size of a cell

# Set up the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTGRAY = (200, 200, 200)
GREEN = (0, 255, 0)


class AbstractPrinter(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def printSudoku(self, board):
        pass


class Printer(AbstractPrinter):
    def __init__(self, board=Board.Board()):
        self.board = numpy.zeros((9, 9), int)
        self.solve = []
        board = board.get_board()
        for i in range(9):
            for j in range(9):
                self.board[i][j] = board[i][j]

    def printSudoku(self, board):
        self.solve = board.get_board()
        global FPSCLOCK, DISPLAYSURF
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Sudoku Solve')

        pygame.font.init()
        font_path = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font_path, CELLSIZE)

        DISPLAYSURF.fill(WHITE)

        self._drawBoard()
        self._drawGrid()
        while True:  # main game loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def _drawGrid(self):

        ### Draw Minor Lines
        for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
            pygame.draw.line(DISPLAYSURF, LIGHTGRAY, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
            pygame.draw.line(DISPLAYSURF, LIGHTGRAY, (0, y), (WINDOWWIDTH, y))

        ### Draw Major Lines
        for x in range(0, WINDOWWIDTH, SQUARESIZE):  # draw vertical lines
            pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, SQUARESIZE):  # draw horizontal lines
            pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (WINDOWWIDTH, y))

        return None

    def _drawBoard(self):
        box_side = WINDOWHEIGHT / 9
        for x in range(9):
            for y in range(9):
                center_x = x * box_side + box_side / 2
                center_y = y * box_side + box_side / 2
                if self.board[x][y] !=0:
                    self.draw_text(str(self.board[x][y]), (center_y, center_x), BLACK)
                else:
                    self.draw_text(str(self.solve[x][y]), (center_y, center_x), GREEN)
        return None

    def draw_text(self, text, center, color=BLACK):
        text = self.font.render(text, True, color)
        rect = text.get_rect()
        rect.center = center
        DISPLAYSURF.blit(text, rect)

if __name__=='__main__':
    board = Board.Board()
    board.put(0, 0, 8)
    board.put(0, 7, 1)
    board.put(1, 1, 5)
    board.put(1, 6, 9)
    board.put(2, 2, 9)
    tab = Printer(board)
    tab.printSudoku()