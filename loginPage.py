from tkinter import *
import json

root = Tk()
root.title("Sign in Page")
root.geometry("800x600")
root.resizable(True, True)
root.configure(bg="#f0f0f0")

frame = Frame(root, bg="white")

frame.pack(pady=40, padx=40,)


def storeInputs():


    file_path = "test.json"
    isRegistered = False
    user_email = email_field.get()
    user_password = password_field.get()
    try:
        with open(file_path, "r") as f:
            file = json.load(f)

        for user in file['users']:
            if user_email == user['email'] and user_password == user['password']:
                isRegistered = True
                break

        if isRegistered:
            email_match_label.config(text="You Are Registered", fg="green")
            password_match_label.config(text="You Are Registered", fg="green")
        else:
            email_match_label.config(text="Account Does Not Exist", fg="red")
            password_match_label.config(text="Account Does Not Exist", fg="red")
    except FileNotFoundError:
        email_match_label.config(text="User database not found!", fg="red")
    

# Toggle password visibility
def isSecure():
    if password_field.cget('show') == '*':
        password_field.config(show='')
        toggle_button.config(text="Hide")
    else:
        password_field.config(show='*')
        toggle_button.config(text="Show")

# UI
title_label = Label(frame, text="WELCOME", font=("Arial", 24, "bold"), fg="#ffffff", bg="#0078d4")
title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

email_label = Label(frame, text="Enter Your Registered Email or Username:", font=("Arial", 12), bg="white")
email_label.grid(row=1, column=0, sticky="w", padx=10, pady=(5, 5))

email_field = Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), width=40, bd=1, relief=SOLID)
email_field.grid(row=2, column=0,sticky="w" ,pady=10, padx=10)

email_match_label = Label(frame, text='', font=("Arial", 10), bg="white")
email_match_label.grid(row=2, column=1, sticky="w")

password_label = Label(frame, text="Enter Your Password:", font=("Arial", 12), bg="white")
password_label.grid(row=3, column=0, sticky="w", padx=10, pady=(5, 5))

password_field = Entry(frame, justify='left', bg="#f7f7f7", font=("Arial", 12), show="*", width=30, bd=1, relief=SOLID)
password_field.grid(row=4, column=0,sticky= 'w' ,pady=10, padx=10)

password_match_label = Label(frame, text='', font=("Arial", 10), bg="white")
password_match_label.grid(row=4, column=1, sticky="w")

toggle_button = Button(frame, text="Show", font=("Arial", 10), relief='flat', bg="#0078d4", fg="white", command=isSecure)
toggle_button.grid(row=4, column=2, padx=10)

signin_button = Button(frame, text="Sign In", font=("Arial", 12), bg="#0078d4", fg="white", relief='flat', width=20, command=storeInputs)
signin_button.grid(row=5, column=0, columnspan=2, pady=(10, 10))

create_account_button = Button(frame, text="Create a New Account", font=("Arial", 10), bg="white", fg="#0078d4", width=20, relief='flat')
create_account_button.grid(row=6, column=0, columnspan=2, pady=(10, 10))

root.mainloop()
