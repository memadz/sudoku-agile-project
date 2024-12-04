import sys
import subprocess
from tkinter import *

def openLoggedInPage():
    logged_in_window = Tk()
    logged_in_window.title("Logged In Page")
    logged_in_window.geometry("800x600")
    logged_in_window.configure(bg="#f0f0f0")

    def playGame():
        subprocess.run([sys.executable, "GUI_V2.py"]) # Must change this to current version

    def logOut():
        logged_in_window.quit()
        logged_in_window.destroy()        
        subprocess.run([sys.executable, "loginPage.py"])

    def settings():
        settings_window = Toplevel(logged_in_window)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        Label(settings_window, text="Settings are coming soon", font=("Arial", 16)).pack(pady=20)

    def showStats():
        stats_window = Toplevel(logged_in_window)
        stats_window.title("Statistics")
        stats_window.geometry("400x300")
        Label(stats_window, text="Statistics are coming soon", font=("Arial", 16)).pack(pady=20)

    def exitApp():
        logged_in_window.quit()

    # UI for the logged-in page
    frame = Frame(logged_in_window, bg="white")
    frame.pack(pady=40, padx=40)

    Label(frame, text="Welcome to the Logged In Page", font=("Arial", 24, "bold"), fg="#ffffff", bg="#0078d4").grid(row=0, column=0, columnspan=2, pady=(10, 20))

    Button(frame, text="Play Sudoku", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=playGame).grid(row=1, column=0, pady=(10, 10))
    Button(frame, text="Settings", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=settings).grid(row=2, column=0, pady=(10, 10))
    Button(frame, text="Statistics", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=showStats).grid(row=3, column=0, pady=(10, 10))
    Button(frame, text="Log Out", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=logOut).grid(row=4, column=0, pady=(10, 10))
    Button(frame, text="Exit", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=exitApp).grid(row=5, column=0, pady=(10, 10))

    logged_in_window.mainloop()

if __name__ == "__main__":
    openLoggedInPage()
