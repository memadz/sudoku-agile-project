import tkinter as tk
import sys, subprocess
import json
from StatisticSaver import update_win_streak



def LoggedInMenu():
    # Get the username directly from the command line argument
    current_username = sys.argv[1]

    def open_difficulty_selection():
        difficulty_window = tk.Toplevel(root)
        difficulty_window.title("Select Difficulty")
        difficulty_window.geometry("400x300")
        difficulty_window.configure(bg="#f0f0f0")

        frame = tk.Frame(difficulty_window, bg="white", padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Select Difficulty", font=("Arial", 18, "bold"), fg="#ffffff", bg="#0078d4").grid(row=0, column=0, columnspan=3, pady=(10, 20))
        tk.Button(frame, text="Continue Game", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=continue_game).grid(row=1, column=0, columnspan=3, pady=(10, 10))
        tk.Button(frame, text="Easy", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=lambda: open_sudoku_game("easy")).grid(row=2, column=0, columnspan=3, pady=(10, 10))
        tk.Button(frame, text="Medium", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=lambda: open_sudoku_game("medium")).grid(row=3, column=0, columnspan=3, pady=(10, 10))
        tk.Button(frame, text="Hard", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=lambda: open_sudoku_game("hard")).grid(row=4, column=0, columnspan=3, pady=(10, 10))

        difficulty_window.grab_set()  # Make the popup window modal (The main root window will become uninteractable)

    def open_sudoku_game(difficulty):
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
            pass

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
        root.destroy()

    # Start point #

    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    # UI for the logged-in page
    frame = tk.Frame(root, bg="white", padx=50, pady=50)
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    tk.Label(frame, text="SUDOKU GAME", font=("Arial", 24, "bold"), fg="#ffffff", bg="#0078d4").grid(row=0, column=0, columnspan=3, pady=(10, 20))
    tk.Button(frame, text="Play Sudoku", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_difficulty_selection).grid(row=1, column=0, columnspan=3, pady=(10, 10))
    tk.Button(frame, text="Settings", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_settings).grid(row=2, column=0, columnspan=3, pady=(10, 10))
    tk.Button(frame, text="Statistics", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_statistics).grid(row=3, column=0, columnspan=3, pady=(10, 10))
    tk.Button(frame, text="Log Out", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_main_menu).grid(row=4, column=0, columnspan=3, pady=(10, 10))
    tk.Button(frame, text="Exit", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=exit_app).grid(row=5, column=0, columnspan=3, pady=(10, 10))

    root.mainloop()

if __name__ == "__main__":
    try:
        LoggedInMenu()
    except Exception:
        print("Please run the main program to access the logged in page.")