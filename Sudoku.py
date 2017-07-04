import SudokuImageReader
import Solver


if __name__ == "__main__":
    image = "sudoku.jpg"
    reader = SudokuImageReader.SudokuImageReader(image)
    sudoku = Solver.Solver(reader.getBoard())
    sudoku.solve()
    sudoku.printSolve()