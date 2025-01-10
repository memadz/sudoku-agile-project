import customtkinter as ctk
import sys, subprocess
import json
from StatisticSaver import update_win_streak

# Main Menu Function
def MainMenu(current_username):

    def open_difficulty_selection(current_username):
        difficulty_window = ctk.CTkToplevel(root)
        difficulty_window.title("Select Difficulty")
        difficulty_window.geometry("400x300")
        difficulty_window.configure(bg="#f0f0f0")

        frame = ctk.CTkFrame(difficulty_window, corner_radius=10, fg_color="#f0f0f0")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        difficulty_label = ctk.CTkLabel(frame, text="Select Difficulty", font=ctk.CTkFont(size=18, weight="bold"), text_color="#333333")
        difficulty_label.pack(pady=(10, 20))

        button_accent = {"fg_color": "#0078D4", "text_color": "#FFFFFF", "hover_color": "#005999"}
        btn_width = 250

        if current_username == "Guest":
            ctk.CTkButton(frame, text="Easy", width= btn_width, command=lambda: open_sudoku_game("Guest", "easy"), **button_accent).pack(pady=3) 
            ctk.CTkButton(frame, text="Medium", width=btn_width, command=lambda: open_sudoku_game("Guest", "medium"), **button_accent).pack(pady=3)
            ctk.CTkButton(frame, text="Hard", width=btn_width, command=lambda: open_sudoku_game("Guest", "hard"), **button_accent).pack(pady=3)
        else:
            ctk.CTkButton(frame, text="Continue", width= btn_width, command=continue_game, **button_accent).pack(pady=3) 
            ctk.CTkButton(frame, text="Easy", width= btn_width, command=lambda: open_sudoku_game(current_username, "easy"), **button_accent).pack(pady=3) 
            ctk.CTkButton(frame, text="Medium", width=btn_width, command=lambda: open_sudoku_game(current_username, "medium"), **button_accent).pack(pady=3)
            ctk.CTkButton(frame, text="Hard", width=btn_width, command=lambda: open_sudoku_game(current_username, "hard"), **button_accent).pack(pady=3)

        difficulty_window.grab_set()  # Make the popup window modal (The main root window will become uninteractable)

    def open_sudoku_game(current_username, difficulty):
        try:
            with open("Users.json", "r") as f:
                users_data = json.load(f)
            user_data = None
            for user in users_data["users"]:
                if user["username"] == current_username:
                    user_data = user
                    break
            if user_data and "game_state" in user_data:
                previous_difficulty = user_data["game_state"]["difficulty"]
                if user_data["game_state"]["lives"] != None or user_data["game_state"]["hint_count"] != None:
                    update_win_streak(current_username, False, previous_difficulty)
        except:
            root.destroy()
            subprocess.run([sys.executable, "Sudoku.py", current_username, difficulty])

        game_state = {
            "difficulty": difficulty,
            "board_state": None, # Placeholder for the board state
            "solved_grid": None # Placeholder for the solved grid
        }
        update_user_game_state(current_username, game_state)
    
        root.destroy()
        subprocess.run([sys.executable, "Sudoku.py", current_username, difficulty]) # Pass the current_username as an argument to the Sudoku file

    def continue_game():
        try:
            with open("Users.json", "r") as f:
                users_data = json.load(f)
            user_data = None
            for user in users_data["users"]:
                if user["username"] == current_username:
                    user_data = user
                    break
            if user_data and "game_state" in user_data:
                if user_data["game_state"]["lives"] != None or user_data["game_state"]["hint_count"] != None: # When losing or winning a game, the value of the key "lives" (or "hint_count") will become None. This prevents the continue option.
                    root.destroy()
                    subprocess.run([sys.executable, "Sudoku.py", current_username, "continue"])
                else:
                    print("Cannot load a finished game.")
            else:
                print("No saved game found.")
        except FileNotFoundError:
            print("No file found")

    def update_user_game_state(username, game_state):
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

    def open_login_page():
        root.destroy()
        subprocess.run([sys.executable, "LoginPage.py"])

    def open_sign_up_page():
        root.destroy()
        subprocess.run([sys.executable, "SignUpPage.py"])

    def open_settings():
        root.destroy()
        subprocess.run([sys.executable, "Settings.py", current_username])

    def open_statistics():
        root.destroy()
        subprocess.run([sys.executable, "StatisticsPage.py", current_username])

    def open_main_menu():
        root.destroy()
        subprocess.run([sys.executable, "MainMenu.py"])

    def exit_app():
        root.quit()
        root.destroy()


    # Start point #
    
    root = ctk.CTk()
    root.title("SUDOKU")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    frame = ctk.CTkFrame(root, corner_radius=0, fg_color="#f0f0f0")
    frame.pack(expand=True, fill="both") # Center the frame

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=3)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(frame, text="SUDOKU", font=ctk.CTkFont(size=36, weight="bold"), text_color="#333333").grid(row=0, column=0, pady=(100, 20), sticky="n")

    button_frame = ctk.CTkFrame(frame, fg_color="#f0f0f0")
    button_frame.grid(row=1, column=0, sticky="nsew")
    button_frame.rowconfigure((0,1,2,3,4), weight=0)
    button_frame.columnconfigure(0, weight=1)

    button_width = 300
    button_font  = ctk.CTkFont(size=20, weight="bold")
    button_accent = {"fg_color": "#0078D4", "text_color": "#FFFFFF", "hover_color": "#005999"}

    if current_username == "Guest":
        ctk.CTkButton(button_frame, text="Play as Guest", command=lambda: open_difficulty_selection(current_username), width=button_width, font=button_font, **button_accent).grid(row=0, column=0, pady=10, sticky="n")
        ctk.CTkButton(button_frame, text="Log In", command=open_login_page, width=button_width, font=button_font, **button_accent).grid(row=1, column=0, pady=10, sticky="n")
        ctk.CTkButton(button_frame, text="Sign Up", command=open_sign_up_page, width=button_width, font=button_font, **button_accent).grid(row=2, column=0, pady=10, sticky="n")
        ctk.CTkButton(button_frame, text="Settings", command=open_settings, width=button_width, font=button_font, **button_accent).grid(row=3, column=0, pady=10, sticky="n")
    else:
        ctk.CTkButton(button_frame, text="Play", command=lambda: open_difficulty_selection(current_username), width=button_width, font=button_font, **button_accent).grid(row=0, column=0, pady=10, sticky="n")
        ctk.CTkButton(button_frame, text="Settings", command=open_settings, width=button_width, font=button_font, **button_accent).grid(row=1, column=0, pady=10, sticky="n")
        ctk.CTkButton(button_frame, text="Statistics", command=open_statistics, width=button_width, font=button_font, **button_accent).grid(row=2, column=0, pady=10, sticky="n")
        ctk.CTkButton(button_frame, text="Log Out", command=open_main_menu, width=button_width, font=button_font, **button_accent).grid(row=3, column=0, pady=10, sticky="n")

    ctk.CTkButton(button_frame, text="Exit", command=exit_app, width=button_width, font=button_font, **button_accent).grid(row=4, column=0, pady=10, sticky="n")

    root.mainloop()

if __name__ == "__main__":
    try:
        current_username = sys.argv[1]
    except Exception:
        current_username = "Guest"

    MainMenu(current_username)
