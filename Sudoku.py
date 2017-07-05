import SudokuImageReader
import Solver
import os
import Printer
from Tkinter import Tk
from tkFileDialog import askopenfilename


if __name__ == "__main__":
    Tk().withdraw()
    filename = askopenfilename(title="Open file", filetypes=[("JPG files", "*.jpg"), ("BMP files", "*.bmp")])
    if os.path.isfile(filename):
        reader = SudokuImageReader.SudokuImageReader(filename)
        printer = Printer.Printer(reader.getBoard())
        sudoku = Solver.Solver(reader.getBoard())
        sudoku.solve()
        sudoku.printSolve()
        printer.printSudoku(sudoku.getBoars())
