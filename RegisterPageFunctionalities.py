import re
import json
import os

# Functionalities for the register page and saving to JSON file (local).

# Regex patterns for username and password (User-defined)
USERNAME_REGEX = r"^[a-zA-Z0-9]{3,20}$"  # 3-20 characters, alphanumeric 
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+{}\[\]:;\"'<>,.?/~`-]).{8,}$" # Contains at least one lowercase letter, one uppercase letter, one digit, one special character and is atleast 8 characters long.

# Declare a filename to save data
filename = "registeredUsers.json"

# Function to save user data to a JSON file
def save_user_data(username, password):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)
    else:
        data = {}
    
    # Save user data
    data[username] = {
        "password": password # Store password
    } 
    
    with open(filename, "w") as file:
        json.dump(data, file, indent=4) # Use indent for readability

# Function to register the user
def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Validate username
    if not re.match(USERNAME_REGEX, username):
        print("Error: Invalid username. Please use 3-20 alphanumeric characters.")
        return
    
    # Validate password
    if not re.match(PASSWORD_REGEX, password):
        print("Error: Password must be at least 8 characters long, include uppercase, lowercase, number, and symbol.")
        return
    
    # Save user data
    save_user_data(username, password)
    print("Registration successful!")

def main():
    register_user() 
if __name__ == "__main__":
    main()
    