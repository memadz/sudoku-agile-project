import tkinter as tk
import json, sys, subprocess

def LoginPage():
    def store_inputs():
        username = username_field.get()
        password = password_field.get()
        try:
            with open("Users.json", "r") as f:
                data = json.load(f)

                for user in data["users"]:
                    if user["username"] == username and user["password"] == password:

                        root.destroy()

                        # Open the LoggedInMenu with the username as an argument
                        subprocess.run([sys.executable, "LoggedInMenu.py", username])

                    else:
                        status_label.config(text="Username or password is incorrect.", fg="red")
                return

        except FileNotFoundError:
            email_match_label.config(text="No users registered yet.", fg="red")
        
    def toggle_password_visibility():
        if password_field.cget('show') == '*':
            password_field.config(show='')
            toggle_button.config(text="Hide")
        else:
            password_field.config(show='*')
            toggle_button.config(text="Show")

    def open_sign_up_page():
        root.destroy()
        subprocess.run([sys.executable, "SignUpPage.py"])

    def go_back():
        root.destroy()
        subprocess.run([sys.executable, "MainMenu.py"])

    # Start point #

    root = tk.Tk()
    root.title("Login Page")
    root.geometry("800x600")
    root.resizable(True, True)
    root.configure(bg="#f0f0f0")

    frame = tk.Frame(root, bg="white")
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    # UI
    title_label = tk.Label(frame, text="Login", font=("Arial", 24, "bold"), fg="#ffffff", bg="#0078d4")
    title_label.grid(row=0, column=0, columnspan=100, pady=(10, 20))

    username_label = tk.Label(frame, text="Enter Your Username:", font=("Arial", 12), bg="white")
    username_label.grid(row=1, column=0, sticky="w", padx=10, pady=(5, 5))

    username_field = tk.Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), width=30, bd=1, relief=tk.SOLID)
    username_field.grid(row=2, column=0,sticky="w" ,pady=10, padx=10)

    email_match_label = tk.Label(frame, text='', font=("Arial", 10), bg="white")
    email_match_label.grid(row=2, column=1, sticky="w")

    password_label = tk.Label(frame, text="Enter Your Password:", font=("Arial", 12), bg="white")
    password_label.grid(row=3, column=0, sticky="w", padx=10, pady=(5, 5))

    password_field = tk.Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), show="*", width=30, bd=1, relief=tk.SOLID)
    password_field.grid(row=4, column=0,sticky= 'w' ,pady=10, padx=10)

    password_match_label = tk.Label(frame, text='', font=("Arial", 10), bg="white")
    password_match_label.grid(row=4, column=1, sticky="w")

    toggle_button = tk.Button(frame, text="Show", font=("Arial", 10), relief='flat', bg="#0078d4", fg="white", command=toggle_password_visibility)
    toggle_button.grid(row=4, column=2, padx=10)

    signin_button = tk.Button(frame, text="Sign In", font=("Arial", 12), bg="#0078d4", fg="white", relief='flat', width=20, command=store_inputs)
    signin_button.grid(row=7, column=0, columnspan=100, pady=(10, 10))

    status_label = tk.Label(frame, text="", font=("Arial", 10), bg="white")
    status_label.grid(row=5, column=0, columnspan=3, pady=(5, 5))

    back_button = tk.Button(frame, text="Back", font=("Arial", 12), bg="#0078d4", fg="white", width=20, command=go_back)
    back_button.grid(row=8, column=0, columnspan=3, pady=(10,10))

    create_account_button = tk.Button(frame, text="Create a New Account", font=("Arial", 10), bg="white", fg="#0078d4", width=20, relief='flat', command=open_sign_up_page)
    create_account_button.grid(row=6, column=0, columnspan=100, pady=(10, 10))

    root.mainloop()

if __name__ == "__main__":
    LoginPage()