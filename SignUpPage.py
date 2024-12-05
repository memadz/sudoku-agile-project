from tkinter import *
import json

root = Tk()
root.title("Sign Up Page")
root.geometry("800x600")
root.resizable(True, True)
root.configure(bg="#f0f0f0")

frame = Frame(root, bg="white")
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

def storeInputs():
    user_email = email_field.get()
    user_password = password_field.get()
    verify_password = verify_password_field.get()
    
    if not user_email or not user_password or not verify_password:
        status_label.config(text="All fields are required.", fg="red")
        return
    
    if user_password != verify_password:
        status_label.config(text="Passwords do not match!", fg="red")
        return

    new_user = {"email": user_email, "password": user_password}

    try:
        with open("test.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"users": []}

    data["users"].append(new_user)

    with open("test.json", "w") as f:
        json.dump(data, f, indent=4)

    status_label.config(text="Account created successfully!", fg="green")

def togglePasswordVisibility(entry_field, toggle_button):
    if entry_field.cget('show') == '*':
        entry_field.config(show='')
        toggle_button.config(text="Hide")
    else:
        entry_field.config(show='*')
        toggle_button.config(text="Show")

def toggleMainPassword():
    togglePasswordVisibility(password_field, password_toggle_button)

def toggleVerifyPassword():
    togglePasswordVisibility(verify_password_field, verify_password_toggle_button)

# UI Elements
title_label = Label(frame, text="CREATE YOUR ACCOUNT", font=("Arial", 24, "bold"), fg="#ffffff", bg="#0078d4")
title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))



email_label = Label(frame, text="Enter Your Email:", font=("Arial", 12), bg="white")
email_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0), padx=10)

email_field = Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), width=40, bd=1, relief=SOLID)
email_field.grid(row=2, column=0, columnspan=2, pady=(0, 10), padx=10)



password_label = Label(frame, text="Enter Your Password:", font=("Arial", 12), bg="white")
password_label.grid(row=3, column=0, columnspan=3, sticky="w", pady=(5, 0), padx=10)

password_field = Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), show="*", width=40, bd=1, relief=SOLID)
password_field.grid(row=4, column=0, columnspan=2, pady=(0, 10), padx=10)

password_toggle_button = Button(frame, text="Show", font=("Arial", 10), relief='flat', bg="#0078d4", fg="white", command=toggleMainPassword)
password_toggle_button.grid(row=4, column=2, pady=(0, 10), padx=10)



verify_password_label = Label(frame, text="Verify Your Password:", font=("Arial", 12), bg="white")
verify_password_label.grid(row=5, column=0, columnspan=3, sticky="w", pady=(5, 0), padx=10)

verify_password_field = Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), show="*", width=40, bd=1, relief=SOLID)
verify_password_field.grid(row=6, column=0, columnspan=2, pady=(0, 10), padx=10)

verify_password_toggle_button = Button(frame, text="Show", font=("Arial", 10), relief='flat', bg="#0078d4", fg="white", command=toggleVerifyPassword)
verify_password_toggle_button.grid(row=6, column=2, pady=(0, 10), padx=10)



signup_button = Button(frame, text="Sign Up", font=("Arial", 12), bg="#0078d4", fg="white", relief='flat', width=20, command=storeInputs)
signup_button.grid(row=7, column=0, columnspan=3, pady=(10, 10))



status_label = Label(frame, text="", font=("Arial", 10), bg="white")
status_label.grid(row=8, column=0, columnspan=3, pady=(5, 5))



login_button = Button(frame, text="Already have an account? Login here.", font=("Arial", 10), bg="white", fg="#0078d4", relief='flat')
login_button.grid(row=9, column=0, columnspan=3, pady=(10, 10))

root.mainloop()
