import tkinter as tk
import sys, subprocess

# Main Menu Function
def MainMenu():
    def open_sign_up_page():
        root.destroy()
        subprocess.run([sys.executable, "SignUpPage.py"])

    def open_login_page():
        root.destroy()
        subprocess.run([sys.executable, "LoginPage.py"])

    def open_sudoku_game():
        root.destroy()
        subprocess.run([sys.executable, "Sudoku.py"])

    def open_settings():
        root.destroy()
        subprocess.run([sys.executable, "Settings.py"])

    def exit_app():
        root.quit()
        root.destroy()


    # Start point #
    
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    frame = tk.Frame(root, bg="white", padx=50, pady=50)
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    tk.Label(frame, text="SUDOKU GAME", font=("Arial", 24, "bold"), fg="#ffffff", bg="#0078d4").grid(row=0, column=0, columnspan=3, pady=(10, 20))
    tk.Button(frame, text="Play as a guest", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_sudoku_game).grid(row=1, column=0, columnspan=3, pady=(10, 10))
    tk.Button(frame, text="Log In", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_login_page).grid(row=2, column=0, columnspan=3, pady=(10, 10))
    tk.Button(frame, text="Sign Up", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_sign_up_page).grid(row=3, column=0, columnspan=3 ,pady=(10, 10))
    tk.Button(frame, text="Settings", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=open_settings).grid(row=4, column=0, columnspan=3, pady=(10, 10))
    tk.Button(frame, text="Exit", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=exit_app).grid(row=5, column=0, columnspan=3, pady=(10, 10))

    root.mainloop()

if __name__ == "__main__":
    MainMenu()
