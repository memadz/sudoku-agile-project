import tkinter as tk
import sys, subprocess
import json


def StatisticsPage():

    # Get the username directly from the command line argument
    current_username = sys.argv[1]

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
    
    # Start point #
    
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("800x750")
    root.configure(bg="#f0f0f0")

    # UI for the logged-in page
    frame = tk.Frame(root, bg="white", padx=50, pady=50)
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    
    # Retrieve the statistics for the current user
    statistics = load_user_statistics(current_username)
    
    # Iterate through each difficulty and display its statistics
    for difficulty in statistics.keys():
        stats = statistics.get(difficulty)
        
        # Create a header for each difficulty
        tk.Label(frame, text=f"{difficulty.capitalize()}", font=("Arial", 10, "bold"), bg="white", fg="black").pack(pady=3)

        # Display the statistics for current difficulty
        tk.Label(frame, text=f"Games Started: {stats["games_started"]}", font=("Arial", 8), bg="white", fg="black").pack(pady=1)
        tk.Label(frame, text=f"Games Won: {stats["games_won"]}", font=("Arial", 8), bg="white", fg="black").pack(pady=1)
        tk.Label(frame, text=f"Win Rate: {float(stats["win_rate"] * 100):.1f}%", font=("Arial", 8), bg="white", fg="black").pack(pady=1)
        tk.Label(frame, text=f"Wins with No Mistakes: {stats['wins_no_mistakes']}", font=("Arial", 8), bg="white", fg="black").pack(pady=1)
        tk.Label(frame, text=f"Current Win Streak: {stats['current_win_streak']}", font=("Arial", 8), bg="white", fg="black").pack(pady=1)
        tk.Label(frame, text=f"Best Win Streak: {stats['best_win_streak']}", font=("Arial", 8), bg="white", fg="black").pack(pady=1)

        # Format best time as MM:SS
        best_time_minutes = int(stats["best_time"] // 60) # Floor division to get the floor value of minutes
        best_time_seconds = int(stats["best_time"] % 60) # Modulo to get the remaining seconds
        tk.Label(frame, text=f"Best Time: {best_time_minutes:02d}:{best_time_seconds:02d}", font=("Arial", 8), bg="white", fg="black").pack(pady=1)

        # Format average time as MM:SS
        average_time_minutes = int(stats["average_time"] // 60)
        average_time_seconds = int(stats["average_time"] % 60)
        tk.Label(frame, text=f"Average Time: {average_time_minutes:02d}:{average_time_seconds:02d}", font=("Arial", 8), bg="white", fg="black").pack(pady=1)

        # Add a separator between different difficulties (optional)
        tk.Label(frame, text="-"*40, font=("Arial", 8), bg="white", fg="black").pack(pady=1)


    def go_back():
        root.destroy()
        subprocess.run([sys.executable, "MainMenu.py", current_username])

    back_button = tk.Button(frame, text="Back", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=go_back)
    back_button.pack(padx=5)


    root.mainloop()

if __name__ == "__main__":
    try:
        StatisticsPage()
    except Exception:
        print("Please run the program in \"MainMenu\" to access the statistics page.")
