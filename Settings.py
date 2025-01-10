import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sys, subprocess, json

def SettingsPage():
    try:
        current_username = sys.argv[1]
    except Exception:
        current_username = "Guest"
    
    root = tk.Tk()
    root.title("Settings")
    root.geometry("800x600")
    root.resizable(True, True)
    root.configure(bg="#f0f0f0")

    frame = ctk.CTkFrame(root, corner_radius=0, fg_color="#f0f0f0")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = ctk.CTkLabel(frame, text="Settings",font=ctk.CTkFont(size=36, weight="bold"), text_color="#333333" )
    title_label.grid(row=0, column=0, columnspan=100, pady=(10, 20))

    try:
        if current_username == "Guest":
            with open("Guest.json", "r") as f:
                data = json.load(f)
                
                current_theme = data["theme"]
                current_font = data["font"]
        else:
            with open("Users.json", "r") as f:
                data = json.load(f)

                for user in data.get("users", []):
                    if user["username"] == current_username:
                        current_theme = user["settings"]["theme"]
                        current_font = user["settings"]["font"]

    except FileNotFoundError:
        current_theme = "Light"
        current_font = "Arial"

    dropdown_theme = tk.StringVar(root)
    dropdown_theme.set(current_theme)

    dropdown_font = tk.StringVar(root)
    dropdown_font.set(current_font)
        
    def update_setting(event=None):
        
        print(f"Theme updated to: {dropdown_theme.get()}")
        print(f"Font updated to: {dropdown_font.get()}")

        if current_username == "Guest":
            with open("Guest.json", "w") as f:
                new_guest = {"theme": dropdown_theme.get(), "font": dropdown_font.get()}
                json.dump(new_guest, f, indent=4)

        else:
            with open("Users.json", "r") as f:
                data = json.load(f)

                for user in data.get("users", []):
                    if user["username"] == current_username:
                        user["settings"]["theme"] = dropdown_theme.get()
                        user["settings"]["font"] = dropdown_font.get()

            with open("Users.json", "w") as f:
                json.dump(data, f, indent=4)
    

    themes = ["Light", "Dark", "Warm", "Dennis"]
    fonts = ["Arial", "NoteWorthy", "Times New Roman", "Courier New", "Verdana"]
    theme_label = tk.Label(frame, text="Theme:", font=("Arial", 12), bg="#f0f0f0", fg="black")
    theme_label.grid(row=1, column=0, columnspan=3, pady=(10, 10))

    theme_dropdown = ttk.Combobox(frame, textvariable=dropdown_theme, values=themes, state="readonly", font=("Arial", 12))
    theme_dropdown.grid(row=2, column=0, columnspan=3, pady=(10, 10))
    theme_dropdown.bind("<<ComboboxSelected>>", update_setting)



    font_label = tk.Label(frame, text="Font:", font=("Arial", 12), bg="#f0f0f0", fg="black")
    font_label.grid(row=3, column=0, columnspan=3, pady=(10, 10))

    font_dropdown = ttk.Combobox(frame, textvariable=dropdown_font, values=fonts, state="readonly", font=("Arial", 12))
    font_dropdown.grid(row=4, column=0, columnspan=3, pady=(10, 10))
    font_dropdown.bind("<<ComboboxSelected>>", update_setting)


    def go_back():
        if current_username == "Guest":
            root.destroy()
            subprocess.run([sys.executable, "MainMenu.py"])
        else:
            root.destroy()
            subprocess.run([sys.executable, "MainMenu.py", current_username])

    back_button = ctk.CTkButton(frame, text="Back", font=("Arial", 18), width=200, fg_color="#0078D4", command=go_back, corner_radius=5)
    back_button.grid(row=8, column=0, columnspan=3, pady=50)

    root.mainloop()

if __name__ == "__main__":
    SettingsPage()
