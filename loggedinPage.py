import tkinter as tk
import sys, subprocess
import json

# Get the username directly from the command line argument
current_username = sys.argv[1]

FILENAME = "test.json"

def load_user_statistics(username):
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file: {e}")
        return None

    for user in data.get("users", []): # Use .get() to avoid KeyError. If key not found, iterate over an empty list.
        if user["username"] == username:
            return user["statistics"] # Retrieve and return the user's statistics for all difficulties
         
    print(f"No matching user is found to {username}")
    return None



def playGame():
    logged_in_window.destroy()
    subprocess.run([sys.executable, "GUI_V2.py", current_username]) # Pass the current_username as an argument to the GUI_V2 file

def settings():
    settings_window = tk.Toplevel(logged_in_window)
    settings_window.title("Settings")
    settings_window.geometry("400x300")
    tk.Label(settings_window, text="Settings are coming soon", font=("Arial", 16)).pack(pady=20)

def showStats():
    stats_window = tk.Toplevel(logged_in_window)
    stats_window.title("Statistics")
    stats_window.geometry("400x300")

    # Retrieve the statistics for the current user
    statistics = load_user_statistics(current_username)
        
    # Iterate through each difficulty and display its statistics
    for difficulty in statistics.keys():
        stats = statistics.get(difficulty)
        
        # Create a header for each difficulty
        tk.Label(stats_window, text=f"{difficulty.capitalize()}", font=("Arial", 14, "bold")).pack(pady=10)

        # Display the statistics for current difficulty
        tk.Label(stats_window, text=f"Games Won: {stats["games_won"]}", font=("Arial", 12)).pack(pady=5)
        tk.Label(stats_window, text=f"Wins with No Mistakes: {stats['wins_no_mistakes']}", font=("Arial", 12)).pack(pady=5)
        tk.Label(stats_window, text=f"Current Win Streak: {stats['current_win_streak']}", font=("Arial", 12)).pack(pady=5)
        tk.Label(stats_window, text=f"Best Win Streak: {stats['best_win_streak']}", font=("Arial", 12)).pack(pady=5)

        # Format best time as MM:SS
        best_time_minutes = int(stats["best_time"] // 60) # Floor division to get the floor value of minutes
        best_time_seconds = int(stats["best_time"] % 60) # Modulo to get the remaining seconds
        tk.Label(stats_window, text=f"Best Time: {best_time_minutes:02d}:{best_time_seconds:02d}", font=("Arial", 12)).pack(pady=5)

        # Format average time as MM:SS
        average_time_minutes = int(stats["average_time"] // 60)
        average_time_seconds = int(stats["average_time"] % 60)
        tk.Label(stats_window, text=f"Average Time: {average_time_minutes:02d}:{average_time_seconds:02d}", font=("Arial", 12)).pack(pady=5)

        # Add a separator between different difficulties (optional)
        tk.Label(stats_window, text="-"*40, font=("Arial", 10)).pack(pady=5)
  

def logOut():
    logged_in_window.destroy()        
    subprocess.run([sys.executable, "MainMenu.py"])

def exitApp():
    logged_in_window.destroy()

# Create the TKinter window for the logged-in page
logged_in_window = tk.Tk()
logged_in_window.title("Logged In Page")
logged_in_window.geometry("800x600")
logged_in_window.configure(bg="#f0f0f0")

# UI for the logged-in page
frame = tk.Frame(logged_in_window, bg="white")
frame.pack(pady=40, padx=40)

tk.Label(frame, text="Welcome to the Logged In Page", font=("Arial", 24, "bold"), fg="#ffffff", bg="#0078d4").grid(row=0, column=0, columnspan=3, pady=(10, 20))
tk.Button(frame, text="Play Sudoku", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=playGame).grid(row=1, column=0, columnspan=3, pady=(10, 10))
tk.Button(frame, text="Settings", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=settings).grid(row=2, column=0, columnspan=3, pady=(10, 10))
tk.Button(frame, text="Statistics", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=showStats).grid(row=3, column=0, columnspan=3, pady=(10, 10))
tk.Button(frame, text="Log Out", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=logOut).grid(row=4, column=0, columnspan=3, pady=(10, 10))
tk.Button(frame, text="Exit", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=exitApp).grid(row=5, column=0, columnspan=3, pady=(10, 10))

logged_in_window.mainloop()

