from tkinter import ttk
import tkinter as tk
import SudokuPuzzleGenerator

GRID_SIZE = 9

def create_gui(root):
    frame = tk.Frame(root)
    frame.pack()

    sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("easy")

    def input_validator(input):
        if input == "":
            return True
        if input.isdigit() and 1 <= int(input) <= 9 and len(input) == 1:
            return True
        else:
            return False

    validation_command = root.register(input_validator)

    sudoku_frame = ttk.Frame(frame, borderwidth=8, relief="ridge", width=800, height=400)
    sudoku_frame.grid()

    entry_widgets = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def insert_numbers(grid):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                entry = tk.Entry(
                    sudoku_frame, 
                    width=2, 
                    justify="center", 
                    font=("Arial", 14), 
                    validate="key", 
                    validatecommand=(validation_command, "%P"), 
                    relief='raised', 
                    borderwidth=5
                )
                entry.grid(row=row, column=col, padx=1, pady=1)
                if grid[row][col] != 0:
                    entry.insert(0, grid[row][col])
                    entry.config(state="readonly")
                entry_widgets[row][col] = entry

    insert_numbers(sudoku_grid)

    def easy_mode():
        nonlocal sudoku_grid, solved_grid
        sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("easy")
        insert_numbers(sudoku_grid)

    def medium_mode():
        nonlocal sudoku_grid, solved_grid
        sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("medium")
        insert_numbers(sudoku_grid)

    def hard_mode():
        nonlocal sudoku_grid, solved_grid
        sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("hard")
        insert_numbers(sudoku_grid)

    def check_solution():
        current = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                user_input = entry_widgets[row][col].get()
                if user_input.isdigit() and int(user_input) == solved_grid[row][col]:
                    current.append(1)
                else:
                    current.append(0)
        if 0 in current:
            print("The puzzle is not solved.")
        else:
            print("Congratulations. The puzzle is solved.")

    def print_grids():
        print("Sudoku Grid")
        for rows in sudoku_grid:
            print(rows)
        print("Solved Grid")
        for rows in solved_grid:
            print(rows)

    button_frame = tk.Frame(root, pady=5)
    button_frame.pack()

    easy_button = tk.Button(button_frame, text="Easy", command=easy_mode)
    easy_button.grid(row=0, column=0, padx=5)

    medium_button = tk.Button(button_frame, text="Medium", command=medium_mode)
    medium_button.grid(row=0, column=1, padx=5)

    hard_button = tk.Button(button_frame, text="Hard", command=hard_mode)
    hard_button.grid(row=0, column=2, padx=5)

    check_button = tk.Button(button_frame, text="Check Puzzle", command=check_solution)
    check_button.grid(row=5, column=1, padx=5)

    print_button = tk.Button(button_frame, text="Print", command=print_grids)
    print_button.grid(row=20, column=1, padx=5)
