import SudokuImageReader
import Solver
import os
from Tkinter import Tk
from tkFileDialog import askopenfilename


if __name__ == "__main__":
    Tk().withdraw()
    filename = askopenfilename(title="Open file", filetypes=[("JPG files", "*.jpg"), ("BMP files", "*.bmp")])
    if os.path.isfile(filename):
        reader = SudokuImageReader.SudokuImageReader(filename)
        sudoku = Solver.Solver(reader.getBoard())
        sudoku.solve()
        sudoku.printSolve()
