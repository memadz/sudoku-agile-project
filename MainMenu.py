import tkinter as tk
import sys, subprocess

# Main Menu Function
def mainMenu():
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    def openSignUp():
        root.destroy()
        subprocess.run([sys.executable, "SignUpPage.py"])

    def openLogInPage():
        root.destroy()
        subprocess.run([sys.executable, "loginPage.py"])

    def playSudoku():
        root.destroy()
        subprocess.run([sys.executable, "GUI_V2.py"])

    def exitApp():
        root.quit()
        root.destroy()

    frame = tk.Frame(root, bg="white")
    frame.pack(pady=40, padx=40)

    tk.Label(frame, text="Welcome to the Sudoku Application", font=("Arial", 24, "bold"), fg="#ffffff", bg="#0078d4").grid(row=0, column=0, columnspan=2, pady=(10, 20))

    tk.Button(frame, text="Sign Up", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=openSignUp).grid(row=1, column=0, pady=(10, 10))
    tk.Button(frame, text="Log In", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=openLogInPage).grid(row=2, column=0, pady=(10, 10))
    tk.Button(frame, text="Play Sudoku", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=playSudoku).grid(row=3, column=0, pady=(10, 10))
    tk.Button(frame, text="Exit", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=exitApp).grid(row=4, column=0, pady=(10, 10))

    root.mainloop()

if __name__ == "__main__":
    mainMenu()
