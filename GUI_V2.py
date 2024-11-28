import tkinter as tk 
import ImplementDifficulties 

root = tk.Tk()
root.title("Sudoku")
root.geometry("300x400")

GRID_SIZE = 9
sudoku_grid = ImplementDifficulties.create_board()  # Start with an empty grid

frame = tk.Frame(root, padx=5, pady=5)
frame.pack(expand=True)

# Function to display the Sudoku grid
def display_sudoku(grid):
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            entry = tk.Entry(frame, width=2, justify="center", font=("Arial", 14))
            entry.grid(row=row, column=col, padx=1, pady=1)

            if grid[row][col] != 0: # If the cell is not empty
                value = grid[row][col] # Then assign the value to that cell // This will call upon the function generate_sudoku_puzzle() from the imported file
            else: # If the cell has the value 0 // This will be true at the start of the program
                value = "" # Then assign "" (nothing) to that cell

            entry.insert(42069, value) # The first argument can be whatever for some reason // probably misunderstanding its functionality

# Functions for each difficulty level
def easy_mode():
    puzzle, solution = ImplementDifficulties.generate_sudoku_puzzle("easy")
    display_sudoku(puzzle)

def medium_mode():
    puzzle, solution = ImplementDifficulties.generate_sudoku_puzzle("medium")
    display_sudoku(puzzle)

def hard_mode():
    puzzle, solution = ImplementDifficulties.generate_sudoku_puzzle("hard")
    display_sudoku(puzzle)

# Create buttons for difficulty levels
button_frame = tk.Frame(root, pady=10)
button_frame.pack()

easy_button = tk.Button(button_frame, text="Easy", command=easy_mode)
easy_button.grid(row=0, column=0, padx=5)

medium_button = tk.Button(button_frame, text="Medium", command=medium_mode)
medium_button.grid(row=0, column=1, padx=5)

hard_button = tk.Button(button_frame, text="Hard", command=hard_mode)
hard_button.grid(row=0, column=2, padx=5)

# Display the initial empty Sudoku grid
display_sudoku(sudoku_grid)

root.mainloop()