import tkinter as tk
from tkinter import ttk
import SudokuPuzzleGenerator
import sys
from SaveStatistics import increment_games_won, increment_wins_no_mistakes, update_win_streak, update_times


# Global variables and constants
GRID_SIZE = 9
sudoku_grid, solved_grid  = SudokuPuzzleGenerator.generate_sudoku_puzzle("easy")
mistake_count = 0

current_username = None
if len(sys.argv) > 1: # Check if there is atleast one command line argument passed
    current_username = sys.argv[1] # Retrieve the username, passed as an argument from loginPage to loggedinPage to GUI_V2
current_difficulty = "easy" # Default to "easy" when the program starts
current_win_streak = {"easy": 0, "medium": 0, "hard": 0,}

time_elapsed = 0
timer_id = None # This is used to controlled the scheduled timer. Keep track of this when pausing/continuing timer

is_solved = False # Variable to track if the puzzle is solved
is_paused = False # Variable to track if the timer is paused

def input_validator(input):
    if input == "":
        return True
    
    if input.isdigit() and 1 <= int(input) <= 9 and len(input) == 1:
        return True
    
    return False

def reset_highlight():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            entry = entry_widgets[row][col]
            entry.config(bg="white", fg="black")

# Highlight current cell and all clashing cells with the same value in its row, column, and 3x3 block.
def highlight_clash(row, col):
    num = entry_widgets[row][col].get()

    for c in range(GRID_SIZE):
        if entry_widgets[row][c].get() == num:
            entry_widgets[row][c].config(bg="white", fg="red")
            
    for r in range(GRID_SIZE):
        if entry_widgets[r][col].get() == num:
            entry_widgets[r][col].config(bg="white", fg="red")

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if entry_widgets[r][c].get() == num:
                entry_widgets[r][c].config(bg="white", fg="red")

def reset_highlight():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            entry = entry_widgets[row][col]
            entry.config(bg="white", fg="black")


# Validate the inputs based on clashes with rows, columns and the 3x3 block.
def validate_input():
    reset_highlight()
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
                    highlight_clash(row, col)
                    errors_found = True
                else:
                    seen.add(num)

    for col in range(GRID_SIZE):
        seen = set()
        for row in range(GRID_SIZE):
            num = user_board[row][col]
            if num != 0:
                if num in seen:
                    highlight_clash(row, col)
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
                            highlight_clash(row, col)
                            errors_found = True
                        else:
                            seen.add(num)

    if not errors_found:
        print("No conflicts found. The inputs are valid.")
    else:
        print("Errors found in the Sudoku inputs.")

# Check user input against the solved grid
def check_input(row, col):
    global mistake_count
    user_input = entry_widgets[row][col].get()
    
    # If the input is incorrect, increment the mistake count
    if user_input.isdigit() and int(user_input) != solved_grid[row][col]:
        mistake_count += 1
        
    return True

# Reset mistake count
def reset_mistake_count():
    global mistake_count
    mistake_count = 0

# Reset win streak if conditions are met
def reset_win_streak():
    global current_username, current_difficulty, current_win_streak, is_solved

    if current_username == None:
        print("No username provided; cannot reset win streak") # Debugging step (can remove)
        return
    
    # Reset the win streak only if the puzzle is not solved
    if not is_solved:
        update_win_streak(current_username, is_solved, current_win_streak, current_difficulty)
        print(f"Win streak for {current_difficulty} has been reset.")
    else:
        print(f"Win streak for {current_difficulty} remains intact.")

# Check if the Sudoku puzzle is solved
def check():
    global is_solved, time_elapsed, current_win_streak
    current = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            user_input = entry_widgets[row][col].get()

            if user_input.isdigit() and int(user_input) == solved_grid[row][col]:
                current.append(1)

            else:
                current.append(0)
            
    if 0 not in current: # If the puzzle is solved
        is_solved = True
        timer("pause") # Stop the timer when the puzzle is solved

        # Check whether if the player is a guest or a registered user.
        if len(sys.argv) > 1: # If more than one argument (username), the player is a user. Otherwise the player is a guest.
            
            # Logic to update statistics after winning
            won = True  # Assuming the user won
            if mistake_count == 0: # If no mistake has been done
                no_mistakes = True
            else:
                no_mistakes = False 
            current_time = time_elapsed # Current time is the time elapsed during the game (in seconds)

            # Update statistics
            increment_games_won(current_username, current_difficulty)
            increment_wins_no_mistakes(current_username, won, no_mistakes, current_difficulty)
            update_win_streak(current_username, won, current_win_streak, current_difficulty)
            update_times(current_username, current_time, current_difficulty)
        
        return True # The puzzle is solved
    else:
        return False # The puzzle is not solved yet
    
# Insert numbers into the Sudoku grid
def insert_numbers(sudoku_grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            entry = tk.Entry(sudoku_frame, width=2, justify="center", font=("Arial", 14), validate="key", validatecommand=(validation_command, "%P"), relief='raised', borderwidth=5)
            entry.grid(row=row, column=col, padx=1, pady=1)
            entry.insert(row, sudoku_grid[row][col])
            entry_widgets[row][col] = entry

            # If the cell is pre-filled, make it read-only
            if sudoku_grid[row][col] != 0:
                entry.insert(0, sudoku_grid[row][col])
                entry.config(state="readonly")  # Make it read-only
            else:
                entry.filled_cell = False  # Cell is empty initially
                entry.bind("<KeyRelease>", on_input) # Event will start upon key release during input, and call the on_input helper function.

# Helper function for input handling
def on_input(event):
    widget = event.widget
    row, col = widget.grid_info()["row"], widget.grid_info()["column"]
    
    user_input = widget.get()
    
    if widget.filled_cell and user_input == "": # If the cell was previously filled (not empty) and is now cleared
        widget.filled_cell = False  # If the cell is cleared, reset filled_cell
    
    if not widget.filled_cell: # If the cell is not filled, proceed to check the input
        
        if user_input and user_input.isdigit() and 1 <= int(user_input) <= 9: # If the user entered a value, mark the cell as filled
            widget.filled_cell = True  # Mark the cell as filled
        elif user_input == "":
            widget.filled_cell = False 

        check_input(row, col)  # Call the check_input function to check for mistakes
    
    check() # Automatically check if the puzzle is solved

    if is_solved:
        print("Congratulations! You have solved the puzzle.")
        
    # If the cell is already filled, do nothing and exit the function early
    else:
        return  # Exit early, no further action needed

# Timer functionality
def timer(action=None):
    global time_elapsed, timer_id, is_paused
    
    if action is None:
        time_elapsed += 1
        minutes = time_elapsed // 60
        seconds = time_elapsed % 60
        formatted_time = f"{minutes:02d}:{seconds:02d}"
        time_label.config(text=f"{formatted_time}")
        
        timer_id = root.after(1000, timer) # Execute timer function every 1000 milliseconds (1 second)
    
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

    elif action == "pause":
        if not is_paused:  # Makes sure it is not paused already
            is_paused = True
            hide_puzzle("hide")
            if timer_id is not None:
                root.after_cancel(timer_id)  # Stop timer updates

    elif action == "continue":
        if is_paused:  # Makes sure it is paused
            is_paused = False
            hide_puzzle("show")
            timer_id = root.after(1000, timer)  # Resume the updates

# Hide or show the puzzle cells
def hide_puzzle(state):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell = entry_widgets[row][col]

            if state == "hide": # Hide the puzzle
                cell.config(state="readonly", show=" ") # Hide the cells by showing a whitespace
            elif state == "show": # Restore the state of the puzzle
                if sudoku_grid[row][col] == 0: # Compared to the unsolved grid
                    cell.config(state="normal", show="")
                else:
                    cell.config(state="readonly", show="")  

# Game modes
def easy_mode():
    global sudoku_grid, solved_grid, current_difficulty, is_solved
    reset_win_streak() # Reset win streak if not solved puzzle
    is_solved = False # Reset the state of the puzzle to not solved
    current_difficulty = "easy" # Set the current difficulty to "easy"
    timer("stop")
    reset_mistake_count() # Reset mistake count
    sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("easy")
    insert_numbers(sudoku_grid)
    timer("start")


def medium_mode():
    global sudoku_grid, solved_grid, current_difficulty, is_solved
    reset_win_streak()
    is_solved = False
    current_difficulty = "medium" # Set the current difficulty to "medium"
    timer("stop")
    reset_mistake_count()  
    sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("medium")
    insert_numbers(sudoku_grid)
    timer("start")


def hard_mode():
    global sudoku_grid, solved_grid, current_difficulty, is_solved
    reset_win_streak()
    is_solved = False
    current_difficulty = "hard" # Set the current difficulty to "hard"
    timer("stop")
    reset_mistake_count()
    sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle("hard")
    insert_numbers(sudoku_grid)
    timer("start")


# Print Sudoku grids for debugging
def print_grids():
    print("Sudoku Grid")
    for rows in sudoku_grid:
        print(rows)
    
    print("Solved Grid")
    for rows in solved_grid:
        print(rows)

# Main program setup
root = tk.Tk()
root.title("Sudoku")
root.geometry("800x800")

frame = tk.Frame(root)
frame.pack()

time_label = tk.Label(root, text="00:00", font=("Arial", 12))
time_label.pack(pady=5)

sudoku_frame = ttk.Frame (frame, borderwidth=8, relief="ridge", width=800, height=400)
sudoku_frame.grid()

entry_widgets = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

validation_command = root.register(input_validator)
insert_numbers(sudoku_grid)
    
# Button frame and setup
button_frame = tk.Frame(root, pady=5)
button_frame.pack()

# Difficulty buttons
easy_button = tk.Button(button_frame, text="Easy", command=easy_mode)
easy_button.grid(row=0, column=0, padx=5)

medium_button = tk.Button(button_frame, text="Medium", command=medium_mode)
medium_button.grid(row=0, column=1, padx=5)

hard_button = tk.Button(button_frame, text="Hard", command=hard_mode)
hard_button.grid(row=0, column=2, padx=5)

# Other functionality buttons
check_button = tk.Button(button_frame, text="Check Puzzle", command=check)
check_button.grid(row=5, column=1, padx=5)

print_button = tk.Button(button_frame, text="Print", command=print_grids)
print_button.grid(row=20, column=1, padx=5)

validate_button = tk.Button(button_frame, text="Validate Inputs", command=validate_input)
validate_button.grid(row=10, column=1, padx=5)

pause_button = tk.Button(button_frame, text="Pause", command=lambda: timer("pause")) # lambda is used here to force parameters, if you dont want to use it then you would need two extra functions
pause_button.grid(row=3, column=0, padx=5)

continue_button = tk.Button(button_frame, text="Continue", command=lambda: timer("continue"))
continue_button.grid(row=3, column=2, padx=5)


root.mainloop()
