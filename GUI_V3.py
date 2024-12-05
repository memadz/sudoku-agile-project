import tkinter as tk
from tkinter import ttk
import SudokuPuzzleGenerator


def launch_sudoku_game():
    for widget in base.winfo_children():
        widget.grid_forget
    
    


    GRID_SIZE = 9


    sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("easy")

    frame = tk.Frame(base)
    frame.pack() 
    



    def input_validator(input):

     if input == "":
        return True
     if input.isdigit() and 1 <= int(input) <= 9 and len(input) == 1:
        return True
     else:
        return False


    validation_command = base.register(input_validator)

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
    
    def easy_mode():
        global sudoku_grid, solved_grid
        sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("easy")
        insert_numbers(sudoku_grid)

    def medium_mode():
        global sudoku_grid, solved_grid
        sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("medium")
        insert_numbers(sudoku_grid)

    def hard_mode():
        global sudoku_grid, solved_grid
        sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("hard")
        insert_numbers(sudoku_grid)

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

    button_frame = tk.Frame(base, pady=5)
    button_frame.pack()

    easy_button = tk.Button(button_frame, text="Easy", command=easy_mode)
    easy_button.grid(row=0, column=0, padx=5)

    medium_button = tk.Button(button_frame, text="Medium", command=medium_mode)
    medium_button.grid(row=0, column=1, padx=5)

    hard_button = tk.Button(button_frame, text="Hard", command=hard_mode)
    hard_button.grid(row=0, column=2, padx=5)

    check_button = tk.Button(button_frame, text="Check Puzzle", command=check)
    check_button.grid(row=5, column=1, padx=5)

    print_button = tk.Button(button_frame, text="Print", command=print_grids)
    print_button.grid(row=20, column=1, padx=5)

def back_to_menu():
    for widget in base.winfo_children():
        widget.grid_forget()

    # add the main menu buttons back
    tk.Button(base, text="Register").pack(pady=20)
    tk.Button(base, text="Log-In").pack(pady=20)
    tk.Button(base, text="Play as Guest", command=launch_sudoku_game).pack(pady=20)  # Opens Sudoku window
    tk.Button(base, text="Settings").pack(pady=20)
    tk.Button(base, text="Exit Main Menu", command=exit_main_menu).pack(pady=20) 

def exit_main_menu():
    base.destroy()
    
        

#create main menu window
base = tk.Tk()
base.title("Sudoku Main Menu")
base.geometry("800x800")

# add button to the  menu
tk.Button(base, text="Register").pack(pady=20)
tk.Button(base, text="Log-In").pack(pady=20)
tk.Button(base, text="Play as Guest", command=launch_sudoku_game).pack(pady=20)  
tk.Button(base, text="Settings").pack(pady=20)
tk.Button(base, text="Exit Main Menu", command=exit_main_menu).pack(pady=20)


base.mainloop()