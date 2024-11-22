import tkinter as tk
import SudokoSolverGenerator

root = tk.Tk()
root.title("Sudoku")
root.geometry("300x400")

GRID_SIZE = 9

sudoku_grid = SudokoSolverGenerator.main()

frame = tk.Frame(root, padx=5, pady=5)
frame.pack(expand=True)

for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        entry = tk.Entry(frame, width=2, justify="center", font=("Arial", 14))
        entry.grid(row=row, column=col, padx=1, pady=1)
        entry.insert(row, sudoku_grid[row][col])
root.mainloop()
