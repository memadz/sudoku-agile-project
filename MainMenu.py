import customtkinter as ctk
import sys, subprocess

def MainMenu():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue") 

    root = ctk.CTk()
    root.title("SUDOKU")
    root.geometry("600x600")
    root.configure(fg_color="#f0f0f0")

    def open_difficulty_selection():
        difficulty_window = ctk.CTkToplevel(root)
        difficulty_window.title("Select Difficulty")
        difficulty_window.geometry("400x300")
        difficulty_window.configure(fg_color="#f0f0f0")

        frame = ctk.CTkFrame(
            difficulty_window,
            corner_radius=10,
            fg_color="#f0f0f0"
        )
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        difficulty_label = ctk.CTkLabel(
            frame,
            text="Select Difficulty",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#333333" 
        )
        difficulty_label.pack(pady=(10, 20))


        button_accent = {
            "fg_color": "#0078D4",
            "text_color": "#FFFFFF",
            "hover_color": "#005999"
        }

        btn_width = 250
        ctk.CTkButton(
            frame, text="Easy",
            font=("Arial", 15),
            width= btn_width,
            command=lambda: open_sudoku_game("Guest", "easy"),
            **button_accent
        ).pack(pady=3) 

        ctk.CTkButton(
            frame, text="Medium",
            font=("Arial", 15),
            width=btn_width,
            command=lambda: open_sudoku_game("Guest", "medium"),
            **button_accent
        ).pack(pady=3)

        ctk.CTkButton(
            frame, text="Hard",
            font=("Arial", 15),
            width=btn_width,
            command=lambda: open_sudoku_game("Guest", "hard"),
            **button_accent
        ).pack(pady=3)

        difficulty_window.grab_set()

    def open_sudoku_game(user, difficulty):
        root.destroy()
        subprocess.run([sys.executable, "Sudoku.py", user, difficulty])

    def open_login_page():
        root.destroy()
        subprocess.run([sys.executable, "LoginPage.py"])

    def open_sign_up_page():
        root.destroy()
        subprocess.run([sys.executable, "SignUpPage.py"])

    def open_settings():
        root.destroy()
        subprocess.run([sys.executable, "Settings.py"])

    def exit_app():
        root.quit()
        root.destroy()

    main_frame = ctk.CTkFrame(
        root,
        corner_radius=0,
        fg_color="#f0f0f0"
    )
    main_frame.pack(expand=True, fill="both")

    main_frame.grid_rowconfigure(0, weight=1) 
    main_frame.grid_rowconfigure(1, weight=3) 
    main_frame.grid_rowconfigure(2, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    title_label = ctk.CTkLabel(
        main_frame,
        text="SUDOKU",
        font=ctk.CTkFont(size=36, weight="bold"),
        text_color="#333333"
    )
    title_label.grid(row=0, column=0, pady=(20, 20), sticky="n")


    buttons_frame = ctk.CTkFrame(main_frame, fg_color="#f0f0f0")
    buttons_frame.grid(row=1, column=0, sticky="nsew")


    buttons_frame.rowconfigure((0,1,2,3,4), weight=0)
    buttons_frame.columnconfigure(0, weight=1)


    button_width = 300
    button_font  = ctk.CTkFont(size=20, weight="bold")
    button_accent = {
        "fg_color": "#0078D4",
        "text_color": "#FFFFFF",
        "hover_color": "#005999"
    }

    ctk.CTkButton(
        buttons_frame, 
        text="Play as Guest", 
        command=open_difficulty_selection, 
        width=button_width, 
        font=button_font,
        **button_accent
    ).grid(row=0, column=0, pady=10, sticky="n")

    ctk.CTkButton(
        buttons_frame, 
        text="Log In", 
        command=open_login_page, 
        width=button_width, 
        font=button_font,
        **button_accent
    ).grid(row=1, column=0, pady=10, sticky="n")

    ctk.CTkButton(
        buttons_frame, 
        text="Sign Up", 
        command=open_sign_up_page, 
        width=button_width, 
        font=button_font,
        **button_accent
    ).grid(row=2, column=0, pady=10, sticky="n")

    ctk.CTkButton(
        buttons_frame, 
        text="Settings", 
        command=open_settings, 
        width=button_width, 
        font=button_font,
        **button_accent
    ).grid(row=3, column=0, pady=10, sticky="n")

    ctk.CTkButton(
        buttons_frame, 
        text="Exit", 
        command=exit_app, 
        width=button_width, 
        font=button_font,
        **button_accent
    ).grid(row=4, column=0, pady=10, sticky="n")

    root.mainloop()

if __name__ == "__main__":
    MainMenu()
