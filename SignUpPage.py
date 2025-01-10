import tkinter as tk
import json, re, sys, subprocess
import customtkinter as ctk

def SignUpPage():
    def store_inputs():
        username = username_field.get()
        password = password_field.get()
        verify_password = verify_password_field.get()
        
        if not username or not password or not verify_password:
            status_label.config(text="All fields are required.", fg="red")
            return
        
        if password != verify_password:
            status_label.config(text="Passwords do not match!", fg="red")
            return
        
        # Validate username
        if not re.match(USERNAME_REGEX, username):
            status_label.config(text="Invalid username. Please use 3-20 alphanumeric characters.", fg="red")
            return
        
        # Validate password
        if not re.match(PASSWORD_REGEX, password):
            status_label.config(text="Password must be at least 8 characters long, include uppercase, lowercase, number, and symbol.", fg="red")
            return

        new_user = {"username": username, 
                    "password": password,
                    "settings": {
                        "theme": "Light",
                        "font": "Arial"
                    },
                    "statistics": {
                        "easy": {
                            "games_started": 0,
                            "games_won": 0,
                            "win_rate": 0,
                            "current_win_streak": 0,
                            "best_win_streak": 0,
                            "wins_no_mistakes": 0,
                            "best_time": 0,
                            "total_time": 0,
                            "average_time": 0
                            },
                        "medium": {
                            "games_started": 0,
                            "games_won": 0,
                            "win_rate": 0,
                            "current_win_streak": 0,
                            "best_win_streak": 0,
                            "wins_no_mistakes": 0,
                            "best_time": 0,
                            "total_time": 0,
                            "average_time": 0
                            },
                        "hard": {
                            "games_started": 0,
                            "games_won": 0,
                            "win_rate": 0,
                            "current_win_streak": 0,
                            "best_win_streak": 0,
                            "wins_no_mistakes": 0,
                            "best_time": 0,
                            "total_time": 0,
                            "average_time": 0
                        }
                    }
        }

        try:
            with open("Users.json", "r") as f:
                data = json.load(f)

                for i in range(len(data["users"])):
                    if data["users"][i]["username"] == username:
                        status_label.config(text="Username already exists.", fg="red")
                        return

        except FileNotFoundError:
            data = {"users": []}

        data["users"].append(new_user)

        with open("Users.json", "w") as f:
            json.dump(data, f, indent=4)

        status_label.config(text="Account created successfully!", fg="green")
        username_field.delete(0, tk.END)
        password_field.delete(0, tk.END)
        verify_password_field.delete(0, tk.END)
        

    def toggle_password_visibility(entry_field, toggle_button):
        if entry_field.cget('show') == '*':
            entry_field.config(show='')
            toggle_button.configure(text="Hide")
        else:
            entry_field.config(show='*')
            toggle_button.configure(text="Show")

    def toggle_main_password():
        toggle_password_visibility(password_field, password_toggle_button)

    def toggle_verify_password():
        toggle_password_visibility(verify_password_field, verify_password_toggle_button)

    def open_login_page():
        root.destroy()
        subprocess.run([sys.executable, "LoginPage.py"])

    def go_back():
        root.destroy()
        subprocess.run([sys.executable, "MainMenu.py"])

    # Start point #

    root = tk.Tk()
    root.title("Sign Up Page")
    root.geometry("800x600")
    root.resizable(True, True)
    root.configure(bg="#f0f0f0")

    frame = tk.Frame(root, bg="#f0f0f0")
    frame.place(relx=0.5, rely=0.5, anchor="center") 

    USERNAME_REGEX = r"^[a-zA-Z0-9]{3,20}$"  # 3-20 characters, alphanumeric 
    PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+{}\[\]:;\"'<>,.?/~`-]).{8,}$" # Contains at least one lowercase letter, one uppercase letter, one digit, one special character and is atleast 8 characters long.

    # UI Elements
    button_width = 200
    button_accent = {"fg_color": "#0078D4", "text_color": "#FFFFFF", "hover_color": "#005999"}

    title_label = ctk.CTkLabel(frame, text="CREATE YOUR ACCOUNT", font=ctk.CTkFont(size=36, weight="bold"), text_color="#333333" )
    title_label.grid(row=0, column=0, columnspan=3, pady=(20, 20))

    username_label = ctk.CTkLabel(frame, text="Enter A Username:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#333333")
    username_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0), padx=10)

    username_field = tk.Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), width=40, bd=1, relief=tk.SOLID)
    username_field.grid(row=2, column=0, columnspan=2, pady=(0, 10), padx=10)

    password_label = ctk.CTkLabel(frame, text="Enter Your Password:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#333333")
    password_label.grid(row=3, column=0, columnspan=3, sticky="w", pady=(5, 0), padx=10)

    password_field = tk.Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), show="*", width=40, bd=1, relief=tk.SOLID)
    password_field.grid(row=4, column=0, columnspan=2, pady=(0, 10), padx=10)

    password_toggle_button = ctk.CTkButton(frame, text="Show", font=("Arial", 16,),text_color="black", bg_color="#f0f0f0", fg_color="#f0f0f0", width=50, command=toggle_main_password)
    password_toggle_button.grid(row=4, column=2, pady=(0, 10), padx=0)

    verify_password_label = ctk.CTkLabel(frame, text="Verify Your Password:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#333333")
    verify_password_label.grid(row=5, column=0, columnspan=3, sticky="w", pady=(5, 0), padx=10)

    verify_password_field = tk.Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), show="*", width=40, bd=1, relief=tk.SOLID)
    verify_password_field.grid(row=6, column=0, columnspan=2, pady=(0, 10), padx=10)

    verify_password_toggle_button = ctk.CTkButton(frame, text="Show", font=("Arial", 16,),text_color="black", bg_color="#f0f0f0", fg_color="#f0f0f0", width=50, command=toggle_verify_password)
    verify_password_toggle_button.grid(row=6, column=2, pady=(0, 10), padx=0)

    signup_button = ctk.CTkButton(frame, text="Sign Up", font=("Arial", 18), width=button_width, **button_accent, command=store_inputs)
    signup_button.grid(row=8, column=0, columnspan=3, pady=(10, 10))

    status_label = tk.Label(frame, text="", font=("Arial", 10), bg="#f0f0f0")
    status_label.grid(row=7, column=0, columnspan=3, pady=(5, 5))

    back_button = ctk.CTkButton(frame, text="Back", font=("Arial", 18), width=button_width, **button_accent, command=go_back)
    back_button.grid(row=9, column=0, columnspan=3, pady=(10,10))

    login_button = tk.Button(frame, text="Already have an account? Login here.", font=("Arial", 10), bg="#f0f0f0", fg="#0078d4", relief='flat', command=open_login_page)
    login_button.grid(row=10, column=0, columnspan=3, pady=(10, 10))

    root.mainloop()

if __name__ == "__main__":
    SignUpPage()
