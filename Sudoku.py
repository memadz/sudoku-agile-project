import tkinter as tk
from tkinter import ttk
import SudokuPuzzleGenerator
import random, sys, subprocess, json, pygame
import customtkinter as ctk
from StatisticSaver import increment_games_started, update_win_rate, increment_games_won, increment_wins_no_mistakes, update_win_streak, update_times

def SudokuGame():
    # Global/Nonlocal variables and constants
    GRID_SIZE = 9
    entry_widgets = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            row.append(None)
        entry_widgets.append(row)
    mistake_count = 0
    hint_count = 0 
    time_elapsed = 0 # Variable to track the time elapsed in seconds
    timer_id = None # This is used to control the scheduled timer. Keep track of this when pausing/continuing timer
    is_solved = False # Variable to track if the puzzle is solved
    is_paused = False # Variable to track if the timer is paused
    lives = 3 # Life system for players
    life_label = None # Label to display the life count
    annotation_mode = False # Variable to track if annotation mode is enabled

    # Default values
    current_username = None # Default username
    current_difficulty = "easy" # Default difficulty
    
    # Initialize the sudoku grid 
    sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle(current_difficulty)

    # Load username and difficulty from command line arguments
    try:
        if len(sys.argv) > 1: # Check if there is atleast one command line argument passed to this file
            current_username = sys.argv[1] # Retrieve the username, passed as an argument from loginPage to loggedinPage to this file
            current_difficulty = sys.argv[2] # Retrieve the difficulty, passed as an argument from loggedinPage to this file
            if sys.argv[1] == "Guest": # If the username is "Guest" (passed from MainMenu.py)
                current_username = None # Set the username to None
    except: # If there are no command line arguments passed
        pass # Do nothing

    # Update certain game statistics immediately if a game is started
    try:
        if current_username != None: 
            increment_games_started(current_username, current_difficulty)
            update_win_rate(current_username, current_difficulty)
    except:
        pass

    # Initialize pygame mixer for sound effects
    pygame.mixer.init()

    sound_background = pygame.mixer.Sound('SFX/background_game_music.wav')
    sound_game_over = pygame.mixer.Sound('SFX/fail_new_game.wav')
    sound_game_over.set_volume(0.5)
    sound_disable = pygame.mixer.Sound('SFX/disable_sound.wav')
    sound_enable = pygame.mixer.Sound('SFX/enable_sound.wav')
    sound_game_start = pygame.mixer.Sound('SFX/new_game_start.wav')
    sound_correct_input = pygame.mixer.Sound('SFX/correct_input_1.wav')
    sound_correct_input.set_volume(0.3)
    sound_incorrect_input = pygame.mixer.Sound('SFX/wrong_input.wav')
    sound_incorrect_input.set_volume(0.3)
    sound_game_completed = pygame.mixer.Sound('SFX/game_completed.wav')
    sound_hint = pygame.mixer.Sound('SFX/hint_sound.wav')
    sound_hint.set_volume(0.3)

    # Initialize the sudoku_grid with tagged numbers to differentiate from user inputs
    def tag_sudoku_grid(sudoku_grid):
        tagged_sudoku_grid = []
        for row in sudoku_grid:
            new_row = []
            for num in row:
                if num != 0:
                    new_row.append([num, "default"])  # Tag default numbers with "default"
                else:
                    new_row.append([0, "default"])  # Tag empty cells with "default"
            tagged_sudoku_grid.append(new_row)
        sudoku_grid = tagged_sudoku_grid
        return sudoku_grid

    # Save game state when needed
    def update_game_state(current_difficulty, sudoku_grid, solved_grid):
        nonlocal time_elapsed, lives, hint_count    
        game_state = {
            "difficulty": current_difficulty,
            "board_state": sudoku_grid,
            "solved_grid": solved_grid,
            "time_elapsed": time_elapsed,
            "lives": lives,
            "hint_count": hint_count,
        }
        save_game_state(current_username, game_state)

    # Open and save the game state to the JSON file
    def save_game_state(username, game_state):
        try:
            with open("Users.json", "r") as f:
                users_data = json.load(f)
            for user in users_data["users"]:
                if user["username"] == username:
                    user["game_state"] = game_state
                    break
            with open("Users.json", "w") as f:
                json.dump(users_data, f, indent=4)
        except FileNotFoundError:
            print("Users.json file not found.")
    
    # Load the game state
    def load_game_state(username):
        try:
            with open("Users.json", "r") as f:
                users_data = json.load(f)
            user_data = None
            for user in users_data["users"]:
                if user["username"] == username:
                    user_data = user
                    break
            if user_data and "game_state" in user_data:
                return user_data["game_state"]
            else:
                return None
        except FileNotFoundError:
            return None

    """ Main game logic functions """
    # Input validation function
    def input_validator(input):
            if input == "":
                return True
            if input.isdigit() and 1 <= int(input) <= 9 and len(input):
                return True
            return False
    
    # Check if the puzzle is solved
    def check():
        nonlocal is_solved, time_elapsed
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
            sound_game_completed.play(fade_ms=2000)
            timer("stop") # Stop the timer when the puzzle is solved

            # Check whether if the player is a guest or a registered user.
            try:
                if current_username != None: # If the player is not a guest
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
                    update_win_rate(current_username, current_difficulty)
                    update_win_streak(current_username, won, current_difficulty)
                    update_times(current_username, current_time, current_difficulty)

                    time_elapsed = 0 # Reset the timer
                    
            except:
                pass

            message_box("win") # Call the message box function with the argument "win"
            
            return True # The puzzle is solved
        else:
            return False # The puzzle is not solved yet
        
    # Check user input for mistakes
    def check_input(row, col):
        nonlocal mistake_count
        user_input = entry_widgets[row][col].get()
        
        # If the input is empty (user has removed input)
        if not user_input:
            reset_highlight()  # Clear previous highlights first
        
        # Check if the input is a digit and within the valid range
        if user_input.isdigit() and 1 <= int(user_input) <= 9:
            # Check if the user input matches the solved grid
            if int(user_input) != solved_grid[row][col]:
                highlight_clash(row, col)
                sound_incorrect_input.play(maxtime=2000)
                update_life()  # Update life count
                mistake_count += 1  # Increment mistake count by 1
            else:
                sound_correct_input.play(maxtime=2000)

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

        
    # Highlight current cell and all clashing cells with the same value in its row, column, and 3x3 block.
    def highlight_clash(row, col):
        user_input = entry_widgets[row][col].get() # Get the current input from the widget

        # Check the specified row and column
        for i in range(GRID_SIZE):
            # Check row
            if entry_widgets[row][i].get() == user_input:
                if entry_widgets[row][i]["state"] != "readonly": # If cell state is not read-only
                    entry_widgets[row][i].config(bg=RELATED_WRONG_CELLS_COLOR, fg=WRONG_INPUT_COLOR, font=ALL_FONTS) # Configurate the background and foreground to red (different hues for distinction)
                else:
                    entry_widgets[row][i].config(readonlybackground=RELATED_WRONG_CELLS_COLOR, fg=FOREGROUND_COLOR, font=ALL_FONTS) # Configurate for read-only cells aswell (foreground is black for distinction)

            # Check column
            if entry_widgets[i][col].get() == user_input:
                if entry_widgets[i][col]["state"] != "readonly":
                    entry_widgets[i][col].config(bg=RELATED_WRONG_CELLS_COLOR, fg=WRONG_INPUT_COLOR, font=ALL_FONTS)
                else:
                    entry_widgets[i][col].config(readonlybackground=RELATED_WRONG_CELLS_COLOR, fg=FOREGROUND_COLOR, font=ALL_FONTS)

        # Check 3x3 block
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if entry_widgets[r][c].get() == user_input:
                    if entry_widgets[r][c]["state"] != "readonly":
                        entry_widgets[r][c].config(bg=RELATED_WRONG_CELLS_COLOR, fg=WRONG_INPUT_COLOR, font=ALL_FONTS)
                    else:
                        entry_widgets[r][c].config(readonlybackground=RELATED_WRONG_CELLS_COLOR, fg=FOREGROUND_COLOR, font=ALL_FONTS)
    
    # Reset highlight function
    def reset_highlight():
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if entry_widgets[row][col]["state"] != "readonly":
                    entry_widgets[row][col].config(bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=ALL_FONTS)
                else:
                    entry_widgets[row][col].config(readonlybackground=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=ALL_FONTS)
                
        # Reapply highlights for all non-empty, non-readonly cells
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                user_input = entry_widgets[row][col].get()
                if user_input and entry_widgets[row][col]["state"] != "readonly":  # Check if the cell is not empty and not readonly
                    if user_input.isdigit() and int(user_input) != solved_grid[row][col]:
                        highlight_clash(row, col)  # Call highlight for non-empty, non-readonly cells
 
    # Function to handle highlighting of cells (Only making this a function since on_click and on_key_press will be using duplicate code otherwise)
    def highlight_related_cells(row, col):
        reset_highlight()  # Clear previous highlights

        # Highlight the entire row and column
        for i in range(GRID_SIZE):
            # Check row
            if entry_widgets[row][i]["state"] != "readonly": # If cell state is not read-only
                if entry_widgets[row][i].cget("bg") != RELATED_WRONG_CELLS_COLOR:  # If the cell has not been marked as a mistake
                    entry_widgets[row][i].config(bg=RELATED_CELLS_COLOR)  # Highlight the background of the cell to blue
            else:
                if entry_widgets[row][i].cget("readonlybackground") != RELATED_WRONG_CELLS_COLOR:
                    entry_widgets[row][i].config(readonlybackground=RELATED_CELLS_COLOR)  # Highlight the background of read-only cells aswell

            # Check column
            if entry_widgets[i][col]["state"] != "readonly":
                if entry_widgets[i][col].cget("bg") != RELATED_WRONG_CELLS_COLOR:
                    entry_widgets[i][col].config(bg=RELATED_CELLS_COLOR)
            else:
                if entry_widgets[i][col].cget("readonlybackground") != RELATED_WRONG_CELLS_COLOR:
                    entry_widgets[i][col].config(readonlybackground=RELATED_CELLS_COLOR)

        # Highlight the 3x3 block
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if entry_widgets[r][c]["state"] != "readonly":
                    if entry_widgets[r][c].cget("bg") != RELATED_WRONG_CELLS_COLOR:
                        entry_widgets[r][c].config(bg=RELATED_CELLS_COLOR)
                else:
                    if entry_widgets[r][c].cget("readonlybackground") != RELATED_WRONG_CELLS_COLOR:
                        entry_widgets[r][c].config(readonlybackground=RELATED_CELLS_COLOR)

        # Highlight the clicked cell
        widget = entry_widgets[row][col]
        if widget["state"] != "readonly":
            widget.config(bg=SELECTED_CELL_COLOR) # Highlight the cell's background to another distinguishable hue of blue
        else:
            widget.config(readonlybackground=SELECTED_CELL_COLOR) # Highlight the read-only cell's background aswell

        # Reapply blue foreground for all correct inputs
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if entry_widgets[r][c]["state"] != "readonly":
                    if entry_widgets[r][c].get() == str(solved_grid[r][c]):
                        entry_widgets[r][c].config(fg=CORRECT_INPUT_COLOR)  # Set text color to blue for correct input

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
                    if entry_widgets[r][c].cget("bg") == RELATED_WRONG_CELLS_COLOR or entry_widgets[r][c].cget("readonlybackground") == RELATED_WRONG_CELLS_COLOR: # If the cell has already been marked a mistake
                        continue # Skip if marked as a mistake
                    if entry_widgets[r][c]["state"] != "readonly" and current_position != (r, c): # If the cell is not read-only
                        entry_widgets[r][c].config(bg=SAME_VALUE_CELL_COLOR) # Highlight the read-only cells with the same value as the clicked cell to another hue of blue for distinction
                    elif entry_widgets[r][c]["state"] == "readonly" and current_position != (r, c): # If the cell is read-only
                        entry_widgets[r][c].config(readonlybackground=SAME_VALUE_CELL_COLOR) # Highlight the cells aswell

    # Reset mistake count
    def reset_mistake_count():
        nonlocal mistake_count
        mistake_count = 0

    # Function to toggle annotation mode
    def toggle_annotation_mode():
        nonlocal annotation_mode

        # Locate the "Note" button
        for widget in button_frame.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Note":
                toggle_annotation_button = widget
                break  # Found the "Note" button, exit the loop

        # Toggle the annotation mode
        annotation_mode = not annotation_mode # True if False, False if True

        if annotation_mode:
            toggle_annotation_button.state(["pressed"])  # ON
            sound_enable.play(maxtime=2000)
        else:
            toggle_annotation_button.state(["!pressed"])  # OFF
            sound_disable.play(maxtime=2000)

    # Update life count for mistakes
    def update_life():
        nonlocal lives, life_label
        lives -= 1  # Decrement the life count by 1 everytime it is called
        if lives > 0:
            life_label.config(text=f"LIVES: {lives}")
        elif lives == 0:
            life_label.config(text=f"")
            sound_game_over.play(maxtime=3000)
            timer("stop")
            message_box("lose") # Call the message box function with the argument "lose"
            
    # Reset lives count
    def reset_lives():
        nonlocal lives, life_label
        # Set back life to 3 whenever it's called
        lives = 3
        life_label.config(text=f"LIVES: {lives}")

    # Give hint to the user
    def give_hint():
        nonlocal hint_count

        if is_paused: # If the timer is paused, don't give hints
            return # Exit the function

        if hint_count >= 3:
            print("Out of hints.")
            sound_incorrect_input.play(maxtime=2000)
            return
        
        empty_cells = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if entry_widgets[row][col].get() == "" or entry_widgets[row][col].cget("fg") == WRONG_INPUT_COLOR:  
                    empty_cells.append((row, col))
        
        if empty_cells:  
            random_cell = random.choice(empty_cells)
            row, col = random_cell
            correct_value = solved_grid[row][col]
            entry_widgets[row][col].delete(0)
            entry_widgets[row][col].insert(0, str(correct_value))
            entry_widgets[row][col].config(state="readonly", readonlybackground=HINT_CELL_COLOR, fg=FOREGROUND_COLOR, font=ALL_FONTS)
            hint_count += 1
            update_game_state(current_difficulty, sudoku_grid, solved_grid) # Not needed, just for visual live update on the JSON file
            highlight_related_cells(row, col)
            sound_hint.play(maxtime=3000)
        else:
            print("No empty cells available for hints.")

        if len(empty_cells) == 1: # If there is only one empty cell left
            check() # Check if the puzzle is solved

    # Reset hint count
    def reset_hint_count():
        nonlocal hint_count
        hint_count = 0
      
    # Reset win streak if conditions are met
    def reset_win_streak():
        nonlocal current_username, current_difficulty, is_solved, time_elapsed

        if current_username == None:
            return # Exit the function if the username is not provided
        
        # Reset the win streak only if the puzzle is not solved
        if not is_solved:
            time_elapsed = 0
            update_game_state(current_difficulty, sudoku_grid, solved_grid)
            update_win_streak(current_username, is_solved, current_difficulty)
            print(f"Win streak for {current_difficulty} has been reset.")
        else:
            print(f"Win streak for {current_difficulty} remains intact.")

    # Function to draw the canvas for the Sudoku grid    
    def draw_grid():
        # Create a canvas over the Sudoku frame for drawing lines
        line_canvas = tk.Canvas(main_frame, width=450, height=450, bg="white", highlightthickness=0)
        line_canvas.grid(row=0, column=0, rowspan=GRID_SIZE, columnspan=GRID_SIZE)
        
        cell_size = 50  # Size of each cell in pixels
        grid_size_px = cell_size * GRID_SIZE  # Total grid size in pixels
        line_width = 2 

        # Draw thick lines to separate 3x3 grids
        for i in range(0, GRID_SIZE + 1):
            # Horizontal lines
            line_canvas.create_line(0, i * cell_size, grid_size_px, i * cell_size, width=line_width, fill=INNER_GRID_LINE_COLOR)

            # Vertical lines
            line_canvas.create_line(i * cell_size, 0, i * cell_size, grid_size_px, width=line_width, fill=INNER_GRID_LINE_COLOR)

        for i in range(0, GRID_SIZE + 1, 3): # Line for distinction of the 3x3's and its in separate loop to ensure it to overlap/overwrite the gray line
            # Horizontal lines
            line_canvas.create_line(0, i * cell_size, grid_size_px, i * cell_size, width=line_width, fill=OUTER_GRID_LINE_COLOR)

            # Vertical lines
            line_canvas.create_line(i * cell_size, 0, i * cell_size, grid_size_px, width=line_width, fill=OUTER_GRID_LINE_COLOR)

    # Insert numbers into the Sudoku grid
    def insert_numbers(sudoku_grid):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                entry = tk.Entry(main_frame, width=2, justify="center", font=ALL_FONTS, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, insertbackground=SELECTED_CELL_COLOR,
                                validate="key", validatecommand=(validation_command, "%P"), relief="flat", borderwidth=2)
                entry.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                entry_widgets[row][col] = entry

                # If the cell is pre-filled, make it read-only
                if sudoku_grid[row][col][0] != 0:
                    entry.insert(0, sudoku_grid[row][col][0]) # Index 0 is the value of the cell
                    entry.config(state="readonly", readonlybackground=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)  # Make it read-only
                    if sudoku_grid[row][col][1] == "wrong": # Tag the value at index 1 with "wrong" for wrong inputs
                        entry.config(state="normal", fg=WRONG_INPUT_COLOR, bg=RELATED_WRONG_CELLS_COLOR) # Make the user input's normal again.
                        entry.filled_cell = True  # Cell is filled initially
                        entry.bind("<KeyPress>", on_key_press) # Bind key press event to call the function "on_key_press"
                    if sudoku_grid[row][col][1] == "correct": # Tag the value at index 1 with "correct" for correct inputs
                        entry.config(state="normal", fg=CORRECT_INPUT_COLOR)
                        entry.filled_cell = True  
                        entry.bind("<KeyPress>", on_key_press) 
                else:
                    entry.filled_cell = False  # Cell is empty initially
                    entry.bind("<KeyPress>", on_key_press) # Bind key press event to call the function "on_key_press"
                entry.bind("<Button-1>", on_click)  # Bind mouse left-click event to call the function "on_click".
                entry.bind("<Tab>", on_tab)  # Bind the tab key to call the function "on_tab"
        
        try:
            if current_username != None: # If the player is not a guest
                highlight_related_cells(row,col) # Highlight related cells for the saved game state
        except:
            pass
                
    # Helper function for key press handling
    def on_key_press(event):
        widget = event.widget
        row, col = widget.grid_info()["row"], widget.grid_info()["column"]

        user_input = event.char

        if annotation_mode:  # If in annotation mode
            if user_input and user_input.isdigit() and 1 <= int(user_input) <= 9:
                widget.delete(0)
                
                # Initialize annotations dictionary if it doesn't exist
                if not hasattr(widget, "annotations"):
                    widget.annotations = {}

                # Check if the annotation already exists
                if user_input in widget.annotations:
                    # Remove the annotation
                    widget.annotations[user_input].destroy() # Destroy the label
                    del widget.annotations[user_input] # Remove the annotation from the dictionary
                else:
                    # Create a label for the annotation
                    annotation_label = tk.Label(widget, text=user_input, font=(ALL_FONTS, 8), fg="#707c8b", bg=widget.cget("bg"), state=tk.NORMAL)

                    # Position the annotation label to cover specific portions of the cell
                    match user_input:
                        case "1":
                            annotation_label.place(relx=0, rely=0, relwidth=0.33, relheight=0.33, anchor="nw")
                        case "2":
                            annotation_label.place(relx=0.5, rely=0, relwidth=0.33, relheight=0.33, anchor="n")
                        case "3":
                            annotation_label.place(relx=1, rely=0, relwidth=0.33, relheight=0.33, anchor="ne")
                        case "4":
                            annotation_label.place(relx=0, rely=0.5, relwidth=0.33, relheight=0.33, anchor="w")
                        case "5":
                            annotation_label.place(relx=0.5, rely=0.5, relwidth=0.33, relheight=0.33, anchor="center")
                        case "6":
                            annotation_label.place(relx=1, rely=0.5, relwidth=0.33, relheight=0.33, anchor="e")
                        case "7":
                            annotation_label.place(relx=0, rely=1, relwidth=0.33, relheight=0.33, anchor="sw")
                        case "8":
                            annotation_label.place(relx=0.5, rely=1, relwidth=0.33, relheight=0.33, anchor="s")
                        case "9":
                            annotation_label.place(relx=1, rely=1, relwidth=0.33, relheight=0.33, anchor="se")

                    # Bind the label click to set focus on the Entry widget
                    annotation_label.bind("<Button-1>", lambda e: (on_click(event), widget.focus_set()))

                    # Automatically reapply highlighting on key press
                    highlight_related_cells(row, col)

                    # Store the annotation label
                    widget.annotations[user_input] = annotation_label
                
            return "break"  # Prevent the key press event from being propagated further (e.g. no input will be added to the Entry widget)
                
        else: # Regular input mode
            # Clear annotations if they exist
            if hasattr(widget, "annotations"):
                for label in widget.annotations.values():
                    label.destroy()
                widget.annotations.clear() # Clear the annotations dictionary for the entry widget
            
            # Check if the input is valid (1-9) or empty
            if user_input and (user_input.isdigit() and 1 <= int(user_input) <= 9):
                if not widget.filled_cell:  # If the cell is not filled, mark it as filled
                    widget.filled_cell = True

                if event.char == widget.get(): # If the input is the same as the previous input
                    widget.delete(0) # Clear the current input
                   
                elif event.char != widget.get(): # If the input is different from the previous input
                    widget.delete(0)
                    widget.insert(0, user_input) # Insert the input into the widget

                check_input(row, col)  # Call the check_input function to check for mistakes

                # Highlight correct input in blue
                if user_input == str(solved_grid[row][col]):  # Check if the input is correct
                    widget.config(fg="#3d5aac")  # Set the text color to blue for correct input
                else:
                    widget.config(fg="red")  # Set to red if incorrect

            elif event.keysym == "BackSpace" and user_input != "": # If the backspace key is pressed
                widget.delete(0) # Clear the current input
    
            if widget.get() == "":  # If the input is cleared
                widget.filled_cell = False  # Reset filled_cell

            # Automatically reapply highlighting on key press
            highlight_related_cells(row, col)

            # Automatically check if the puzzle is solved
            check()

            if is_solved:
                print("Congratulations! You have solved the puzzle!")

            # Update the board state and save the game state
            if current_username != None: # If the player is not a guest
                try:
                    value = widget.get()
                    if widget.get() == "":  # If the input is empty
                        value = 0
                        sudoku_grid[row][col][1] = "default"
                        sudoku_grid[row][col][0] = value
                    else:
                        value = int(widget.get()) # Convert the input to an integer
                        sudoku_grid[row][col][0] = value
                
                    if widget.cget("fg") == WRONG_INPUT_COLOR:
                        sudoku_grid[row][col][1] = "wrong"
                    if widget.cget("fg") == CORRECT_INPUT_COLOR:
                        sudoku_grid[row][col][1] = "correct"

                    update_game_state(current_difficulty, sudoku_grid, solved_grid)
                except ValueError:
                    sudoku_grid[row][col][0] = 0

            return "break"  # Prevent the key press event from being propagated further (e.g. no input will be added to the Entry widget)
  
    # Helper function for mouse left-click handling
    def on_click(event):
        widget = event.widget
        row, col = widget.grid_info()["row"], widget.grid_info()["column"]

        # Automatically reapply highlighting on left-click
        highlight_related_cells(row, col)

        # Update the background color of the existing annotation labels
        for row_widgets in entry_widgets: # Iterate through each row of entry widgets (list of lists)
            for entry_widget in row_widgets: # Iterate through each entry widget in the row (element of the list)
                if hasattr(entry_widget, "annotations"):
                    entry_bg_color = entry_widget.cget("bg")  # Get the background color of the Entry widget the label belongs to
                    for label in entry_widget.annotations.values():
                        try:
                            label.config(bg=entry_bg_color)
                        except tk.TclError: # Handle the case where the label no longer exists
                            pass

    # Helper function for tab key press handling
    def on_tab(event):
        widget = event.widget
        next_widget = widget.tk_focusNext()
        while next_widget and not isinstance(next_widget, tk.Entry): # Keep looping until the next widget is an Entry widget (prevent tabbing to other widgets and buttons)
            next_widget = next_widget.tk_focusNext() 
        if next_widget and isinstance(next_widget, tk.Entry):
            next_widget.focus()
            # Create a synthetic event to pass to on_click
            synthetic_event = tk.Event()
            synthetic_event.widget = next_widget
            on_click(synthetic_event)  # Call the on_click function for the new widget
        return "break"  # Prevent the default behavior of tab key press event from being propagated further (e.g., stop the default tabbing behavior, use the custom defined behavior instead)
    
    # Timer functionality
    def timer(action=None):
        nonlocal time_elapsed, timer_id, is_paused
        
        if action is None:
            time_elapsed += 1
            minutes = time_elapsed // 60
            seconds = time_elapsed % 60
            formatted_time = f"{minutes:02d}:{seconds:02d}"
            time_label.config(text=f"{formatted_time}")
            
            timer_id = root.after(1000, timer) # Execute timer function every 1000 milliseconds (1 second)

        elif action == "start":
            time_elapsed = 0
            try:
                game_state = load_game_state(current_username)
                time_elapsed = game_state["time_elapsed"]
                time_label.config(text=f"{time_elapsed // 60:02d}:{time_elapsed % 60:02d}")
            except:
                time_label.config(text="00:00")
            if timer_id is not None:
                root.after_cancel(timer_id)
            timer_id = root.after(1000, timer)
        
        elif action == "stop":
            if timer_id is not None:
                root.after_cancel(timer_id)
                timer_id = None

    def toggle_pause_continue():
        nonlocal is_paused, timer_id

        # Locate the "Pause/continue" button
        for widget in button_frame.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Pause" or widget.cget("text") == "Continue":
                toggle_pause_continue = widget
                break  # Found the button, exit the loop

        is_paused = not is_paused # True if False, False if True

        if is_paused:
            sound_disable.play(maxtime=2000)
            hide_puzzle("hide")
            if timer_id is not None:
                root.after_cancel(timer_id)  # Stop timer updates
            toggle_pause_continue.config(text="Continue")
        else:
            sound_enable.play(maxtime=2000)
            hide_puzzle("show")
            timer_id = root.after(1000, timer)  # Resume the updates
            toggle_pause_continue.config(text="Pause")

    # Hide or show the puzzle cells
    def hide_puzzle(state):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = entry_widgets[row][col]

                if state == "hide": # Hide the puzzle
                    cell.config(state="disabled", disabledbackground=BACKGROUND_COLOR, show=" ") # Hide the cells by showing a whitespace
                    cell.unbind("<Button-1>") # Unbind left click to make sure cells are not interactive
                    cell.unbind("<KeyPress>") # Unbind key press
                    cell.unbind("<Tab>") # Unbind tab key
                elif state == "show": # Restore the state of the puzzle
                   
                    if sudoku_grid[row][col][1] == "wrong" or sudoku_grid[row][col][1] == "correct" or sudoku_grid[row][col][0] == 0:
                        cell.config(state="normal", show="")
                    else:
                        cell.config(state="readonly", show="") 
           
                    cell.bind("<Button-1>", on_click) # Rebind left click
                    cell.bind("<KeyPress>", on_key_press) # Rebind key press
                    cell.bind("<Tab>", on_tab) # Rebind tab key  

    # Message box popup for different game states
    def message_box(gamestate):
        # Make sure these variables exist in the outer scope or pass them as needed
        nonlocal game_state, time_elapsed, lives, hint_count

        # Disable interaction with the main window
        root.focus()
        root.attributes("-disabled", True,)
        
        # Create the popup window
        popup_window = ctk.CTkToplevel(root)
        popup_window.geometry("400x300")
        popup_window.resizable(False, False)
        popup_window.configure(fg_color="#f0f0f0")
        popup_window.protocol("WM_DELETE_WINDOW", lambda: None)  # Prevent closing via "X" button

        # (Optional) If you want to hide/disable window decorations:
        # popup_window.overrideredirect(True)

        # Define a consistent style for labels
        label_font = ctk.CTkFont(size=14, weight="normal")
        label_color = "#333333"

        # Define a consistent style for buttons
        button_accent = {
            "fg_color": "#0078D4",
            "text_color": "#FFFFFF",
            "hover_color": "#005999"
        }
        button_width = 200
        button_font = ctk.CTkFont(size=12, weight="bold")

        # Helper function to close and re-enable the root
        def close_popup():
            root.attributes("-disabled", False)
            popup_window.destroy()

        # Handle different game states
        if gamestate == "win":
            lives = None
            hint_count = None
            update_game_state(current_difficulty, sudoku_grid, solved_grid)

            popup_window.title("Congratulations!")
            ctk.CTkLabel(
                popup_window,
                text="Congratulations! You won the game!",
                font=label_font,
                text_color=label_color
            ).pack(pady=20)

            ctk.CTkLabel(
                popup_window,
                text="Choose a new game",
                font=label_font,
                text_color=label_color
            ).pack(pady=15)

        elif gamestate == "lose":
            lives = None
            hint_count = None
            update_game_state(current_difficulty, sudoku_grid, solved_grid)
            reset_win_streak()

            popup_window.title("Game Over")
            ctk.CTkLabel(
                popup_window,
                text="You ran out of lives! Better Luck Next Time.",
                font=label_font,
                text_color=label_color
            ).pack(pady=20)

            ctk.CTkLabel(
                popup_window,
                text="Choose a new game",
                font=label_font,
                text_color=label_color
            ).pack(pady=15)

        elif gamestate == "newgame":
            popup_window.title("New Game")
            ctk.CTkLabel(
                popup_window,
                text="Choose a new game",
                font=label_font,
                text_color=label_color
            ).pack(pady=15)

            close_btn = ctk.CTkButton(
                popup_window,
                text="Close",
                width=button_width,
                font=button_font,
                command=close_popup,
                **button_accent
            )
            close_btn.pack(pady=5)

        # Easy Mode Button
        if gamestate == "newgame":
            # If "newgame", reset streak before changing mode
            easy_btn = ctk.CTkButton(
                popup_window,
                text="Easy Mode",
                width=button_width,
                font=button_font,
                command=lambda: [
                    reset_win_streak(),
                    change_mode("easy"),
                    close_popup()
                ],
                **button_accent
            )
        else:
            # Otherwise, go straight to changing mode
            easy_btn = ctk.CTkButton(
                popup_window,
                text="Easy Mode",
                width=button_width,
                font=button_font,
                command=lambda: [
                    change_mode("easy"),
                    close_popup()
                ],
                **button_accent
            )
        easy_btn.pack(pady=5)

        # Medium Mode Button
        if gamestate == "newgame":
            medium_btn = ctk.CTkButton(
                popup_window,
                text="Medium Mode",
                width=button_width,
                font=button_font,
                command=lambda: [
                    reset_win_streak(),
                    change_mode("medium"),
                    close_popup()
                ],
                **button_accent
            )
        else:
            medium_btn = ctk.CTkButton(
                popup_window,
                text="Medium Mode",
                width=button_width,
                font=button_font,
                command=lambda: [
                    change_mode("medium"),
                    close_popup()
                ],
                **button_accent
            )
        medium_btn.pack(pady=5)

        # Hard Mode Button
        if gamestate == "newgame":
            hard_btn = ctk.CTkButton(
                popup_window,
                text="Hard Mode",
                width=button_width,
                font=button_font,
                command=lambda: [
                    reset_win_streak(),
                    change_mode("hard"),
                    close_popup()
                ],
                **button_accent
            )
        else:
            hard_btn = ctk.CTkButton(
                popup_window,
                text="Hard Mode",
                width=button_width,
                font=button_font,
                command=lambda: [
                    change_mode("hard"),
                    close_popup()
                ],
                **button_accent
            )
        hard_btn.pack(pady=5)

        # Main Menu Button
        # If you want a distinct color for this "Main Menu" button, you can set it here
        main_menu_btn = ctk.CTkButton(
            popup_window,
            text="Main Menu",
            width=button_width,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="red",
            text_color="black",
            hover_color="#cc0000",
            command=lambda: [go_back(), root.destroy()]
        )
        main_menu_btn.pack(pady=10)


    # Game modes
    def change_mode(mode):
        nonlocal sudoku_grid, solved_grid, current_difficulty, is_solved, is_paused, game_state, current_username
        sound_game_start.play(maxtime=3000)
        reset_win_streak() # Reset win streak if not solved puzzle
        is_solved = False # Reset the state of the puzzle to not solved 
        is_paused = False # Reset the state of the timer to not paused
        current_difficulty = mode # Set the global variable to the current mode
        timer("stop")
        reset_mistake_count() # Reset the mistake count
        reset_hint_count() # Reset the hint count
        reset_lives() # Reset the lives
        sudoku_grid, solved_grid = SudokuPuzzleGenerator.generate_sudoku_puzzle(mode)
        sudoku_grid = tag_sudoku_grid(sudoku_grid)
        insert_numbers(sudoku_grid)
        timer("start")

        if current_username != None: # If the player is a registered user
            increment_games_started(current_username, current_difficulty) # Update game statistics
            update_win_rate(current_username, current_difficulty) 
            update_game_state(current_difficulty, sudoku_grid, solved_grid) # Update game state

    # Print Sudoku grids for debugging or answers. Remove comment on line 974 to use.
    def print_grids():
        print("Sudoku Grid")
        for rows in sudoku_grid:
            print(rows)
        
        print("Solved Grid")
        for rows in solved_grid:
            print(rows)

    def on_closing():
        update_game_state(current_difficulty, sudoku_grid, solved_grid)
        root.destroy() # Destroy the root window

    # Function to go back to the designated menu
    def go_back():
        if current_username == None:
            root.destroy()
            subprocess.run([sys.executable, "MainMenu.py"])
        else:
            on_closing()
            subprocess.run([sys.executable, "MainMenu.py", current_username])

    # Required setup for the game to run
    try:
        if current_username == None: # Declare the theme/font based on the user settings
            with open("Guest.json", "r") as f:
                data = json.load(f)
                theme = data["theme"]
                font = data["font"]
        else:
            with open("Users.json", "r") as f:
                data = json.load(f)
                for user in data.get("users", []):
                    if user["username"] == current_username:
                        theme = user["settings"]["theme"]
                        font = user["settings"]["font"]

            if current_difficulty == "continue":
                game_state = load_game_state(current_username)
                if game_state:
                    current_difficulty = game_state["difficulty"]
                    board_state = game_state["board_state"]
                    solved_grid_state = game_state["solved_grid"]
                    time_elapsed = game_state["time_elapsed"]
                    lives = game_state["lives"]
                    hint_count = game_state["hint_count"]
                else:
                    print("No saved game found.")
                    return

    except FileNotFoundError: # If there are no files, default theme is set.
        theme = "Light"
        font = "Arial"

    match theme:
        case "Light":
            ROOT_BACKGROUND_COLOR = "#f0f0f0"
            BACKGROUND_COLOR = "white" # Cell bg
            FOREGROUND_COLOR = "black" # Text color

            INNER_GRID_LINE_COLOR = "#c0c6d3"
            OUTER_GRID_LINE_COLOR = "black"

            RELATED_CELLS_COLOR = "#e8ecf4" # Same row/col/3x3 cells
            RELATED_WRONG_CELLS_COLOR = "#f7cfd6"
            SELECTED_CELL_COLOR = "#c1ddf9" # The cell currently clicked
            SAME_VALUE_CELL_COLOR = "#c6d7e9" # Cells with the same VALUE as the selected cell

            CORRECT_INPUT_COLOR = "#3d5aac" # If correct input
            WRONG_INPUT_COLOR = "#f80310" # If wrong input
            HINT_CELL_COLOR = "#c1ddf9" # Hint cell color

        case "Dark":
            ROOT_BACKGROUND_COLOR = "#16151b"
            BACKGROUND_COLOR = "#25242c"
            FOREGROUND_COLOR = "#838c9b"

            INNER_GRID_LINE_COLOR = "#1e1e22"
            OUTER_GRID_LINE_COLOR = "#000000"

            RELATED_CELLS_COLOR = "#16151b"
            RELATED_WRONG_CELLS_COLOR = "#6b000a"
            SELECTED_CELL_COLOR = "#003c7b"
            SAME_VALUE_CELL_COLOR = "#000000"

            CORRECT_INPUT_COLOR = "#6a8fc6"
            WRONG_INPUT_COLOR = "#e90039"
            HINT_CELL_COLOR = "#003c7b"

        case "Warm":
            ROOT_BACKGROUND_COLOR = "#f3ead9"
            BACKGROUND_COLOR = "#f3ead9"
            FOREGROUND_COLOR = "#5a4f48"

            INNER_GRID_LINE_COLOR = "#c8c5c0"
            OUTER_GRID_LINE_COLOR = "#403933"

            RELATED_CELLS_COLOR = "#ebdbc1"
            RELATED_WRONG_CELLS_COLOR = "#ffccd5"
            SELECTED_CELL_COLOR = "#b2dffe"
            SAME_VALUE_CELL_COLOR = "#d7c4a6"

            CORRECT_INPUT_COLOR = "#0e47a1"
            WRONG_INPUT_COLOR = "#e90039"
            HINT_CELL_COLOR = "#b2dffe"

        case "Dennis":
            ROOT_BACKGROUND_COLOR = "#1f1f1f"
            BACKGROUND_COLOR = "#28292f"
            FOREGROUND_COLOR = "#bfbfbf"

            INNER_GRID_LINE_COLOR = "#3a3a3a"
            OUTER_GRID_LINE_COLOR = "#bfbfbf"

            RELATED_CELLS_COLOR = "#3a425f"
            RELATED_WRONG_CELLS_COLOR = "#402429"
            SELECTED_CELL_COLOR = "#24293b"
            SAME_VALUE_CELL_COLOR = "#2c3247"

            CORRECT_INPUT_COLOR = "#79b1ff"
            WRONG_INPUT_COLOR = "#910109"
            HINT_CELL_COLOR = "#24293b" 

    match font:
        case "Arial":
            ALL_FONTS = ("Arial", 20)
        case "NoteWorthy":
            ALL_FONTS = ("NoteWorthy", 20)
        case "Times New Roman":
            ALL_FONTS = ("Times New Roman", 20)
        case "Courier New":
            ALL_FONTS = ("Courier New", 20)
        case "Verdana":
            ALL_FONTS = ("Verdana", 20)

    # Start point of the game
    root = tk.Tk()
    root.title("Sudoku")
    root.geometry("900x700")
    root.config(bg=ROOT_BACKGROUND_COLOR)
    try:
        if current_username != None: # If the player is not a guest
            root.protocol("WM_DELETE_WINDOW", on_closing) # Call the on_closing function when the window is closed
    except:
        pass

    main_frame = tk.Frame(root, bg=ROOT_BACKGROUND_COLOR)
    main_frame.pack()

    life_label = tk.Label(main_frame, text=f"LIVES: {lives}", font=("Arial", 10), bg=ROOT_BACKGROUND_COLOR, fg="red")
    life_label.grid(row=GRID_SIZE, sticky='e', column=6, columnspan=GRID_SIZE, pady=10) 

    time_label = tk.Label(main_frame, text="00:00", bg=ROOT_BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=ALL_FONTS)
    time_label.grid(row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE)

    button_frame = tk.Frame(main_frame, bg=ROOT_BACKGROUND_COLOR)
    button_frame.grid(row=GRID_SIZE + 2, column=0, columnspan=GRID_SIZE)

    style = ttk.Style()
    style.configure("TButton", background=ROOT_BACKGROUND_COLOR, foreground="black")
    style.map("TButton",
          background=[("pressed", ROOT_BACKGROUND_COLOR)],
          foreground=[("pressed", "black")])

    ttk.Button(button_frame, text="Pause", style = "TButton", command=toggle_pause_continue).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="Note", style = "TButton", command=toggle_annotation_mode).grid(row=0, column=1, padx=5)
    ttk.Button(button_frame, text="Hint", style = "TButton", command=give_hint).grid(row=0, column=2, padx=5)
    ttk.Button(button_frame, text="Back", style = "TButton", command=go_back).grid(row=1, column=0, padx=5)
    ttk.Button(button_frame, text="New Game", style = "TButton", command=lambda: message_box("newgame")).grid(row=1, column=2, padx=5)
    #ttk.Button(button_frame, text="Print", style = "TButton", command=print_grids).grid(row=2, column=1, padx=5) # Uncomment to enable button.

    # When the program starts, the puzzle is shown directly. Those are the necessary functions for that to happen.
    validation_command = root.register(input_validator)
    draw_grid()
    try:
        if board_state: # If the board state is not empty
            sudoku_grid = board_state  # Load the saved board state
        if solved_grid_state: # If the solved grid state is not empty
            solved_grid = solved_grid_state  # Load the saved solved grid state
    except:
        sudoku_grid = tag_sudoku_grid(sudoku_grid)
    insert_numbers(sudoku_grid)
    try:
        if current_username != None:
            update_game_state(current_difficulty, sudoku_grid, solved_grid)
    except:
        pass
    timer("start")

    root.mainloop()

if __name__ == "__main__":
    SudokuGame()
    
