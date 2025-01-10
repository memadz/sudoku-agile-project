import tkinter as tk
import json, sys, subprocess
import customtkinter as ctk

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

                        subprocess.run([sys.executable, "MainMenu.py", username])

                    else:
                        status_label.config(text="Username or password is incorrect.", fg="red")
                return

        except FileNotFoundError:
            status_label.config(text="No users registered yet.", fg="red")
        
    def toggle_password_visibility():
        if password_field.cget('show') == '*':
            password_field.config(show='')
            toggle_button.configure(text="Hide")
        else:
            password_field.config(show='*')
            toggle_button.configure(text="Show")

    def open_sign_up_page():
        root.destroy()
        subprocess.run([sys.executable, "SignUpPage.py"])

    def go_back():
        root.destroy()
        subprocess.run([sys.executable, "MainMenu.py"])


    root = tk.Tk()
    root.title("Login Page")
    root.geometry("800x600")
    root.resizable(True, True)
    root.configure(bg="#f0f0f0")

    frame = tk.Frame(root, bg="#f0f0f0")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # UI
    button_width = 200
    button_accent = {"fg_color": "#0078D4", "text_color": "#FFFFFF", "hover_color": "#005999"}

    title_label = ctk.CTkLabel(frame, text="LOGIN",font=ctk.CTkFont(size=36, weight="bold"), text_color="#333333" )
    title_label.grid(row=0, column=0, columnspan=100, pady=(10, 20))

    username_label = tk.Label(frame, text="Enter Your Username:", font=("Arial", 12), bg="#f0f0f0")
    username_label.grid(row=1, column=0, sticky="w", padx=10, pady=(5, 5))

    username_field = tk.Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), width=40, bd=1, relief=tk.SOLID)
    username_field.grid(row=2, column=0,sticky="w" ,pady=10, padx=10)

    password_label = tk.Label(frame, text="Enter Your Password:", font=("Arial", 12), bg="#f0f0f0")
    password_label.grid(row=3, column=0, sticky="w", padx=10, pady=(5, 5))

    password_field = tk.Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), show="*", width=40, bd=1, relief=tk.SOLID)
    password_field.grid(row=4, column=0,sticky= 'w' ,pady=10, padx=10)

    toggle_button = ctk.CTkButton(frame, text="Show", font=("Arial", 16,),text_color="black", bg_color="#f0f0f0", fg_color="#f0f0f0", width=50, command=toggle_password_visibility)
    toggle_button.grid(row=4, column=2)

    signin_button = ctk.CTkButton(frame, text="Sign In", font=("Arial", 18), width=button_width, **button_accent, command=store_inputs)
    signin_button.grid(row=8, column=0, columnspan=3, pady=(10,10))

    status_label = tk.Label(frame, text="", font=("Arial", 10), bg="#f0f0f0")
    status_label.grid(row=5, column=0, columnspan=3, pady=(5, 5))

    back_button = ctk.CTkButton(frame, text="Back", font=("Arial", 18), width=button_width, **button_accent, command=go_back)
    back_button.grid(row=9, column=0, columnspan=3, pady=(10,10))

    create_account_button = tk.Button(frame, text="Create a New Account", font=("Arial", 10), bg="#f0f0f0", fg="#0078d4", width=20, relief='flat', command=open_sign_up_page)
    create_account_button.grid(row=10, column=0, columnspan=100, pady=(10, 10))

    root.mainloop()

if __name__ == "__main__":
    LoginPage()
