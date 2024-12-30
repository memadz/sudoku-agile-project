import random
import tkinter as tk
from tkinter import ttk
import SudokuPuzzleGenerator
import sys
from SaveStatistics import increment_games_won, increment_wins_no_mistakes, update_win_streak, update_times


# Global variables and constants
GRID_SIZE = 9
ALL_FONTS = ("Arial", 20)
sudoku_grid, solved_grid  = SudokuPuzzleGenerator.generate_sudoku_puzzle("easy")
mistake_count = 0
hint_count = 0

current_username = None
if len(sys.argv) > 1: # Check if there is atleast one command line argument passed
    current_username = sys.argv[1] # Retrieve the username, passed as an argument from loginPage to loggedinPage to this file
current_difficulty = "easy" # Default to "easy" when the program starts
current_win_streak = {"easy": 0, "medium": 0, "hard": 0,}

time_elapsed = 0
timer_id = None # This is used to controlled the scheduled timer. Keep track of this when pausing/continuing timer

is_solved = False # Variable to track if the puzzle is solved
is_paused = False # Variable to track if the timer is paused


lives = 3
life_label = None
def setup_life_system():
    global life_label
    life_label = tk.Label(sudoku_frame, text=f"LIVES : {lives}", font=("Arial", 10), fg="red")
    life_label.grid(row=GRID_SIZE, sticky='e',column=6,columnspan=GRID_SIZE,pady=10) 

# Pop up box for new game options
def message_box():
    root.attributes('-disabled', 1) # Disables the grid from interaction
    popup_window = tk.Toplevel()
    popup_window.title("Game Over")

    popup_window.geometry("400x300")
    popup_window.resizable(False, False)  # Restrict Resize

    popup_window.protocol("WM_DELETE_WINDOW", lambda: True) # Disable delete window
    popup_window.attributes("-toolwindow", True) # Disable windows tools
    
    tk.Label(popup_window, text="You ran out of lives! Better Luck Next Time", font=("Arial", 12)).pack(pady=20)
    tk.Label(popup_window, text="Choose a new game", font=("Arial", 12)).pack(pady=15)

    # Easy Mode Button
    easy_button = tk.Button(popup_window, text="Easy Mode", font=("Arial", 12), command=lambda: [easy_mode(), root.attributes('-disabled', 0), popup_window.destroy()]) # Call easy mode, re-enable the root and destroy the popup in this order.
    easy_button.pack(padx=20, pady=5)

    # Medium Mode Button
    medium_button = tk.Button(popup_window, text="Medium Mode", font=("Arial", 12), command=lambda: [medium_mode(), root.attributes('-disabled', 0), popup_window.destroy()])
    medium_button.pack(padx=20, pady=5)

    # Hard Mode Button
    hard_button = tk.Button(popup_window, text="Hard Mode", font=("Arial", 12), command=lambda: [hard_mode(), root.attributes('-disabled', 0), popup_window.destroy()])
    hard_button.pack(padx=20, pady=5)

# Life System for players
def mistake_handler():
    global lives
    global life_label
    # Decrement the life everytime it is called
    lives -=1
    if lives >0:
        life_label.config(text=f" LIVES = {lives}")
    # If the player is out of life it will pop up a message window
    elif lives ==0:
        life_label.config(text=f"")
        timer("stop")
        message_box()
        
def reset_lives():
    global lives
    global life_label
    # Set back life to 3 whenever it's called
    lives = 3
    life_label.config(text=f" LIVES: {lives}")

def input_validator(input):
    if input == "":
        return True
    
    if input.isdigit() and 1 <= int(input) <= 9 and len(input) == 1:
        return True
    
    return False

# Highlight current cell and all clashing cells with the same value in its row, column, and 3x3 block.
def highlight_clash(row, col):
    user_input = entry_widgets[row][col].get() # Get the current input from the widget

    # Check the specified row and column
    for i in range(GRID_SIZE):
        # Check row
        if entry_widgets[row][i].get() == user_input:
            if entry_widgets[row][i]["state"] != "readonly": # If cell state is not read-only
                entry_widgets[row][i].config(bg="#f7cfd6", fg="red", font=ALL_FONTS) # Configurate the background and foreground to red (different hues for distinction)
            else:
                entry_widgets[row][i].config(readonlybackground="#f7cfd6", fg="black", font=ALL_FONTS) # Configurate for read-only cells aswell (foreground is black for distinction)

        # Check column
        if entry_widgets[i][col].get() == user_input:
            if entry_widgets[i][col]["state"] != "readonly":
                entry_widgets[i][col].config(bg="#f7cfd6", fg="red", font=ALL_FONTS)
            else:
                entry_widgets[i][col].config(readonlybackground="#f7cfd6", fg="black", font=ALL_FONTS)

    # Check 3x3 block
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if entry_widgets[r][c].get() == user_input:
                if entry_widgets[r][c]["state"] != "readonly":
                    entry_widgets[r][c].config(bg="#f7cfd6", fg="red", font=ALL_FONTS)
                else:
                    entry_widgets[r][c].config(readonlybackground="#f7cfd6", fg="black", font=ALL_FONTS)

def reset_highlight():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if entry_widgets[row][col]["state"] != "readonly":
                entry_widgets[row][col].config(bg="white", fg="black", font=ALL_FONTS)
            else:
                entry_widgets[row][col].config(readonlybackground="white", fg="black", font=ALL_FONTS)
            
    # Reapply highlights for all non-empty, non-readonly cells
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            user_input = entry_widgets[row][col].get()
            if user_input and entry_widgets[row][col]["state"] != "readonly":  # Check if the cell is not empty and not readonly
                if user_input.isdigit() and int(user_input) != solved_grid[row][col]:
                    highlight_clash(row, col)  # Call highlight for non-empty, non-readonly cells
  
# Check user input for mistakes
def check_input(row, col):
    global mistake_count
    user_input = entry_widgets[row][col].get()
    
    # If the input is empty (user has removed input)
    if not user_input:
        reset_highlight()  # Clear previous highlights first
    
    # Check if the input is a digit and within the valid range
    if user_input.isdigit() and 1 <= int(user_input) <= 9:
        # Check if the user input matches the solved grid
        if int(user_input) != solved_grid[row][col]:
            highlight_clash(row, col)
            mistake_handler()  # Call the highlight clash function
            mistake_count += 1  # Increment mistake count by 1

        # Check for duplicates in the same row and column
        for i in range(GRID_SIZE):
            if i != col and entry_widgets[row][i].get() == user_input: # Check for duplicates in the same row
                highlight_clash(row, i)  # Highlight duplicate in the row
        
            if i != row and entry_widgets[i][col].get() == user_input: # Check for duplicates in the same column
                highlight_clash(i, col)  # Highlight duplicate in the column

        # Check for duplicates in the same 3x3 block
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r != row or c != col) and entry_widgets[r][c].get() == user_input:
                    highlight_clash(r, c)  # Highlight duplicate in the block

# Reset mistake count
def reset_mistake_count():
    global mistake_count
    mistake_count = 0
    
# reset hint count
def reset_hint_count():
    global hint_count
    hint_count = 0

def give_hint():
    global hint_count 
    if hint_count >= 3:
        print("Out of hints.")
        return
    
    empty_cells = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if entry_widgets[row][col].get() == "":  
                empty_cells.append((row, col))

    if empty_cells:  
        random_cell = random.choice(empty_cells)
        row, col = random_cell
        correct_value = solved_grid[row][col]
        entry_widgets[row][col].delete(0, tk.END)
        entry_widgets[row][col].insert(0, str(correct_value))
        entry_widgets[row][col].config(state="readonly", readonlybackground="yellow", fg="black", font=ALL_FONTS)
        hint_count += 1
    else:
        print("No empty cells available for hints.")


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
    
def draw_grid():
    # Create a canvas over the Sudoku frame for drawing lines
    line_canvas = tk.Canvas(sudoku_frame, width=450, height=450, bg="white", highlightthickness=0)
    line_canvas.grid(row=0, column=0, rowspan=GRID_SIZE, columnspan=GRID_SIZE)
    
    cell_size = 50  # Size of each cell in pixels
    grid_size_px = cell_size * GRID_SIZE  # Total grid size in pixels
    line_width = 2 

    # Draw thick lines to separate 3x3 grids
    for i in range(0, GRID_SIZE + 1):
        color = "#c0c6d3" # Lightgray color
        
        # Horizontal lines
        line_canvas.create_line(0, i * cell_size, grid_size_px, i * cell_size, width=line_width, fill=color)

        # Vertical lines
        line_canvas.create_line(i * cell_size, 0, i * cell_size, grid_size_px, width=line_width, fill=color)

    for i in range(0, GRID_SIZE + 1, 3):
        color = "black" # Black line for distinction of the 3x3's and its in separate loop to ensure black will overlap/overwrite the gray line
        
        # Horizontal lines
        line_canvas.create_line(0, i * cell_size, grid_size_px, i * cell_size, width=line_width, fill=color)

        # Vertical lines
        line_canvas.create_line(i * cell_size, 0, i * cell_size, grid_size_px, width=line_width, fill=color)

# Insert numbers into the Sudoku grid
def insert_numbers(sudoku_grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            entry = tk.Entry(sudoku_frame, width=2, justify="center", font=ALL_FONTS, validate="key", validatecommand=(validation_command, "%P"), 
                             relief="flat", borderwidth=2)
            entry.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            entry_widgets[row][col] = entry

            # If the cell is pre-filled, make it read-only
            if sudoku_grid[row][col] != 0:
                entry.insert(0, sudoku_grid[row][col])
                entry.config(state="readonly", readonlybackground="white", fg="black")  # Make it read-only
            else:
                entry.filled_cell = False  # Cell is empty initially
                entry.bind("<KeyRelease>", on_input) # Bind key release event to call the function "on_input".
            entry.bind("<Button-1>", on_click)  # Bind mouse left-click event to call the function "on_click".
                
# Helper function for input handling
def on_input(event):
    widget = event.widget
    row, col = widget.grid_info()["row"], widget.grid_info()["column"]

    user_input = widget.get()

    # Check if the input is valid (1-9) or empty
    if user_input and (user_input.isdigit() and 1 <= int(user_input) <= 9):
        if not widget.filled_cell:  # If the cell is not filled, mark it as filled
            widget.filled_cell = True

        check_input(row, col)  # Call the check_input function to check for mistakes

        # Highlight correct input in blue
        if user_input == str(solved_grid[row][col]):  # Check if the input is correct
            widget.config(fg="#3d5aac")  # Set the text color to blue for correct input
        else:
            widget.config(fg="red")  # Set to red if incorrect

    elif user_input == "":  # If the input is cleared
        widget.filled_cell = False  # Reset filled_cell

    # Automatically reapply highlighting on keyboard release
    highlight_related_cells(row, col)

    # Automatically check if the puzzle is solved
    check()

    if is_solved:
        print("Congratulations! You have solved the puzzle!")

# Helper function for mouse left-click handling
def on_click(event):
    widget = event.widget
    row, col = widget.grid_info()["row"], widget.grid_info()["column"]
    
    # Automatically reapply highlighting on left-click
    highlight_related_cells(row, col)

# Function to handle highlighting of cells (Only making this a function since on_click and on_input will be using duplicate code otherwise)
def highlight_related_cells(row, col):
    reset_highlight()  # Clear previous highlights

    # Highlight the entire row and column
    for i in range(GRID_SIZE):
        # Check row
        if entry_widgets[row][i]["state"] != "readonly": # If cell state is not read-only
            if entry_widgets[row][i].cget("bg") != "#f7cfd6":  # If the cell has not been marked as a mistake
                entry_widgets[row][i].config(bg="#e8ecf4")  # Highlight the background of the cell to blue
        else:
            if entry_widgets[row][i].cget("readonlybackground") != "#f7cfd6":
                entry_widgets[row][i].config(readonlybackground="#e8ecf4")  # Highlight the background of read-only cells aswell

        # Check column
        if entry_widgets[i][col]["state"] != "readonly":
            if entry_widgets[i][col].cget("bg") != "#f7cfd6":
                entry_widgets[i][col].config(bg="#e8ecf4")
        else:
            if entry_widgets[i][col].cget("readonlybackground") != "#f7cfd6":
                entry_widgets[i][col].config(readonlybackground="#e8ecf4")

    # Highlight the 3x3 block
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if entry_widgets[r][c]["state"] != "readonly":
                if entry_widgets[r][c].cget("bg") != "#f7cfd6":
                    entry_widgets[r][c].config(bg="#e8ecf4")
            else:
                if entry_widgets[r][c].cget("readonlybackground") != "#f7cfd6":
                    entry_widgets[r][c].config(readonlybackground="#e8ecf4")

    # Highlight the clicked cell
    widget = entry_widgets[row][col]
    if widget["state"] != "readonly":
        widget.config(bg="#c1ddf9") # Highlight the cell's background to another distinguishable hue of blue
    else:
        widget.config(readonlybackground="#c1ddf9") # Highlight the read-only cell's background aswell

    # Reapply blue foreground for all correct inputs
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if entry_widgets[r][c]["state"] != "readonly":
                if entry_widgets[r][c].get() == str(solved_grid[r][c]):
                    entry_widgets[r][c].config(fg="#3d5aac")  # Set text color to blue for correct input

    # Get the value from the clicked cell
    user_input = widget.get()
    
    # If the cell is not empty, highlight all cells with the same value
    if user_input and user_input.isdigit():
        highlight_all_same_value(user_input, row, col) # Pass the value of the clicked cell and its position


# Function to highlight all cells with the same value
def highlight_all_same_value(value, row, col):
    current_position = (row, col)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if entry_widgets[r][c].get() == value:
                if entry_widgets[r][c].cget("bg") == "#f7cfd6" or entry_widgets[r][c].cget("readonlybackground") == "#f7cfd6": # If the cell has already been marked a mistake
                    continue # Skip if marked as a mistake
                if entry_widgets[r][c]["state"] != "readonly" and current_position != (r, c): # If the cell is not read-only
                    entry_widgets[r][c].config(bg="#c6d7e9") # Highlight the read-only cells with the same value as the clicked cell to another hue of blue for distinction
                elif entry_widgets[r][c]["state"] == "readonly" and current_position != (r, c): # If the cell is read-only
                    entry_widgets[r][c].config(readonlybackground="#c6d7e9") # Highlight the cells aswell

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
    reset_hint_count()
    setup_life_system()
    reset_lives()
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
    reset_hint_count()
    setup_life_system()
    reset_lives()
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
    reset_hint_count()
    setup_life_system()
    reset_lives()
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

time_label = tk.Label(root, text="00:00", font=ALL_FONTS)
time_label.pack(pady=5)

sudoku_frame = ttk.Frame (frame, borderwidth=8, relief="ridge", width=800, height=400)
sudoku_frame.grid()

entry_widgets = []
for i in range(GRID_SIZE):
    row = []
    for j in range(GRID_SIZE):
        row.append(None)
    entry_widgets.append(row)

# When the program starts, the puzzle is shown directly. We are calling these functions here immediately for that reason.
validation_command = root.register(input_validator)
draw_grid()
insert_numbers(sudoku_grid)
setup_life_system()
timer("start")
    
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

pause_button = tk.Button(button_frame, text="Pause", command=lambda: timer("pause")) # lambda is used here to force parameters, if you dont want to use it then you would need two extra functions
pause_button.grid(row=3, column=0, padx=5)

hint_button = tk.Button(sudoku_frame, text="Hint", command=give_hint)
hint_button.grid(row=GRID_SIZE, column=0,columnspan=GRID_SIZE,pady=10)

continue_button = tk.Button(button_frame, text="Continue", command=lambda: timer("continue"))
continue_button.grid(row=3, column=2, padx=5)

root.mainloop()