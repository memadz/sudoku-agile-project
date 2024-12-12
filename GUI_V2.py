import tkinter as tk
from tkinter import ttk
import SudokuPuzzleGenerator

root = tk.Tk()
root.title("Sudoku")
root.geometry("800x800")

GRID_SIZE = 9

sudoku_grid, solved_grid  = SudokuPuzzleGenerator.generate_sudoku_puzzle("easy")


frame = tk.Frame(root)
frame.pack()



def input_validator(input):

    if input == "":
        return True
    if input.isdigit() and 1 <= int(input) <= 9 and len(input) == 1:
        return True
    else:
        return False


# Validate the inputs based on clashes with rows, columns and the subgrid
def validate_input():
    user_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            user_input = entry_widgets[row][col].get()
            if user_input.isdigit():
                user_board[row][col] = int(user_input)

    errors_found = False

    for row in range(GRID_SIZE):
        seen = set()
        for col in range(GRID_SIZE):
            num = user_board[row][col]
            if num != 0:
                if num in seen:
                    print(f"Row conflict found at cell ({row+1}, {col+1}) with number {num}")
                    errors_found = True
                else:
                    seen.add(num)

    for col in range(GRID_SIZE):
        seen = set()
        for row in range(GRID_SIZE):
            num = user_board[row][col]
            if num != 0:
                if num in seen:
                    print(f"Column conflict found at cell ({row+1}, {col+1}) with number {num}")
                    errors_found = True
                else:
                    seen.add(num)

    for i in range(0, GRID_SIZE, 3):
        for j in range(0, GRID_SIZE, 3):
            seen = set()
            for row in range(i, i + 3):
                for col in range(j, j + 3):
                    num = user_board[row][col]
                    if num != 0:
                        if num in seen:
                            print(f"Subgrid conflict found at cell ({row+1}, {col+1}) with number {num}")
                            errors_found = True
                        else:
                            seen.add(num)

    if not errors_found:
        print("No conflicts found. The inputs are valid.")
    else:
        print("Errors found in the Sudoku inputs.")

validation_command = root.register(input_validator)

sudoku_frame = ttk.Frame (frame, borderwidth=8, relief="ridge", width=800, height=400)
sudoku_frame.grid()

entry_widgets = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def insert_numbers(sudoku_grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            entry = tk.Entry(sudoku_frame, width=2, justify="center", font=("Arial", 14), validate="key", validatecommand=(validation_command, "%P"), relief='raised', borderwidth=5)
            entry.grid(row=row, column=col, padx=1, pady=1)
            entry.insert(row, sudoku_grid[row][col])
            entry_widgets[row][col] = entry

            if sudoku_grid[row][col] != 0:
                entry.insert(0, sudoku_grid[row][col])
                entry.config(state="readonly")

insert_numbers(sudoku_grid)

time_label = tk.Label(root, text="00:00", font=("Arial", 12))
time_label.pack(pady=5)

time_elapsed = 0
timer_id = None #This is used to controlled the scheduled timer. Keep track of this when pusing/playing timer

def timer(action=None):
    global time_elapsed, timer_id
    
    if action is None:
        time_elapsed += 1
        minutes = time_elapsed // 60
        seconds = time_elapsed % 60
        formatted_time = f"{minutes:02d}:{seconds:02d}"
        time_label.config(text=f"{formatted_time}")
        
        timer_id = root.after(1000, timer)
    
    elif action == "start":
        time_elapsed = 0
        time_label.config(text="00:00")
        if timer_id is not None:
            root.after_cancel(timer_id)
        timer_id = root.after(1000, timer)
    
    elif action == "stop":
        if timer_id is not None:
            root.after_cancel(timer_id)
            timer_id = None

    
def easy_mode():
    global sudoku_grid, solved_grid
    timer("stop")
    sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("easy")
    insert_numbers(sudoku_grid)
    timer("start")

def medium_mode():
    global sudoku_grid, solved_grid
    timer("stop")
    sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("medium")
    insert_numbers(sudoku_grid)
    timer("start")

def hard_mode():
    global sudoku_grid, solved_grid
    timer("stop")
    sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("hard")
    insert_numbers(sudoku_grid)
    timer("start")

def check():

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

    print(current)
            
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

check_button = tk.Button(button_frame, text="Check Puzzle", command=check)
check_button.grid(row=5, column=1, padx=5)

validate_button = tk.Button(button_frame, text="Validate Inputs", command=validate_input)
validate_button.grid(row=10, column=1, padx=5)

print_button = tk.Button(button_frame, text="Print", command=print_grids)
print_button.grid(row=20, column=1, padx=5)

root.mainloop()
