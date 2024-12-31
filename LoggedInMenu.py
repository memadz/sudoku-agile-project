import tkinter as tk
import sys, subprocess
import json

# Get the username directly from the command line argument
current_username = sys.argv[1]


def LoggedInMenu():
    def load_user_statistics(username):
        try:
            with open("Users.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading file: {e}")
            return None

        for user in data.get("users", []): # Use .get() to avoid KeyError. If key not found, iterate over an empty list.
            if user["username"] == username:
                return user["statistics"] # Retrieve and return the user's statistics for all difficulties
            
        print(f"No matching user is found to {username}")
        return None

    def open_sudoku_game():
        root.destroy()
        subprocess.run([sys.executable, "Sudoku.py", current_username]) # Pass the current_username as an argument to the Sudoku file

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
    tk.Button(frame, text="Play Sudoku", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_sudoku_game).grid(row=1, column=0, columnspan=3, pady=(10, 10))
    tk.Button(frame, text="Settings", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_settings).grid(row=2, column=0, columnspan=3, pady=(10, 10))
    tk.Button(frame, text="Statistics", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_statistics).grid(row=3, column=0, columnspan=3, pady=(10, 10))
    tk.Button(frame, text="Log Out", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_main_menu).grid(row=4, column=0, columnspan=3, pady=(10, 10))
    tk.Button(frame, text="Exit", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=exit_app).grid(row=5, column=0, columnspan=3, pady=(10, 10))

    root.mainloop()

if __name__ == "__main__":
    LoggedInMenu()