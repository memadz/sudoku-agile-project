import tkinter as tk
import json, sys, subprocess

root = tk.Tk()
root.title("Login Page")
root.geometry("800x600")
root.resizable(True, True)
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="white")

frame.pack(pady=40, padx=40,)


def storeInputs():
    username = username_field.get()
    password = password_field.get()
    try:
        with open("test.json", "r") as f:
            data = json.load(f)

            for user in data["users"]:
                if user["username"] == username and user["password"] == password:

                    root.destroy()

                    # Call loggedinPage.py with the username as an argument
                    subprocess.run([sys.executable, "loggedinPage.py", username])

                else:
                    status_label.config(text="Username or password is incorrect.", fg="red")
            return

    except FileNotFoundError:
        email_match_label.config(text="No users registered yet.", fg="red")
    

# Toggle password visibility
def isSecure():
    if password_field.cget('show') == '*':
        password_field.config(show='')
        toggle_button.config(text="Hide")
    else:
        password_field.config(show='*')
        toggle_button.config(text="Show")


def go_to_signup():
    root.destroy()
    subprocess.run([sys.executable, "SignUpPage.py"])

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



toggle_button = tk.Button(frame, text="Show", font=("Arial", 10), relief='flat', bg="#0078d4", fg="white", command=isSecure)
toggle_button.grid(row=4, column=2, padx=10)



signin_button = tk.Button(frame, text="Sign In", font=("Arial", 12), bg="#0078d4", fg="white", relief='flat', width=20, command=storeInputs)
signin_button.grid(row=7, column=0, columnspan=100, pady=(10, 10))



status_label = tk.Label(frame, text="", font=("Arial", 10), bg="white")
status_label.grid(row=5, column=0, columnspan=3, pady=(5, 5))



create_account_button = tk.Button(frame, text="Create a New Account", font=("Arial", 10), bg="white", fg="#0078d4", width=20, relief='flat', command=go_to_signup)
create_account_button.grid(row=6, column=0, columnspan=100, pady=(10, 10))

root.mainloop()
