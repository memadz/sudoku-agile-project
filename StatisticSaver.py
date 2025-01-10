import json

FILENAME = "Users.json"

def load_user_statistics(username, current_difficulty):
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file: {e}")
        return None

    for user in data.get("users", []): # Use .get() to avoid KeyError. If key not found, iterate over an empty list.
        if user["username"] == username:
            # Return the statistics for the specified difficulty
            return user["statistics"][current_difficulty] # Retrieve and return the user's statistics
         
    print(f"No matching user is found to {username}")
    return None

        
def save_user_statistics(username, statistics, current_difficulty):
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file: {e}")
        return
    
    user_found = False
    for user in data.get("users", []):
        if user["username"] == username:
            user["statistics"][current_difficulty] = statistics
            user_found = True
            break

    if user_found:
        try:
            with open(FILENAME, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving file: {e}")
    else:
        print(f"User '{username}' not found. Statistics not saved.")

def increment_games_started(username, current_difficulty):
    statistics = load_user_statistics(username, current_difficulty) # Call the load function, store the values in variable "statistics"
    statistics["games_started"] += 1 # Increment by 1 when game is won.
    save_user_statistics(username, statistics, current_difficulty) # Call the save function, save the statistics.

def update_win_rate(username, current_difficulty):
    statistics = load_user_statistics(username, current_difficulty) # Call the load function, store the values in variable "statistics"
    statistics["win_rate"] = statistics["games_won"] / statistics["games_started"]
    save_user_statistics(username, statistics, current_difficulty) # Call the save function, save the statistics.


def increment_games_won(username, current_difficulty):
    statistics = load_user_statistics(username, current_difficulty) # Call the load function, store the values in variable "statistics"
    statistics["games_won"] += 1 # Increment by 1 when game is won.
    save_user_statistics(username, statistics, current_difficulty) # Call the save function, save the statistics.


def increment_wins_no_mistakes(username, won, no_mistakes, current_difficulty):
    statistics = load_user_statistics(username, current_difficulty)
    if won and no_mistakes:
        statistics["wins_no_mistakes"] += 1
    save_user_statistics(username, statistics, current_difficulty)


def update_win_streak(username, won, current_difficulty):
    statistics = load_user_statistics(username, current_difficulty)

    if won:
        statistics["current_win_streak"] += 1
    else:
        statistics["current_win_streak"] = 0 # If lose, reset win streak to 0.

    if statistics["current_win_streak"] >= statistics["best_win_streak"]:
        statistics["best_win_streak"] = statistics["current_win_streak"]
        
    save_user_statistics(username, statistics, current_difficulty)


def update_times(username, current_time, current_difficulty):
    statistics = load_user_statistics(username, current_difficulty)

    # Update best time
    if statistics["best_time"] == 0 or current_time < statistics["best_time"]:
        statistics["best_time"] = current_time # Store the best time

    # Update total time
    statistics["total_time"] += current_time

    # Calculate average time
    statistics["average_time"] = statistics["total_time"] / statistics["games_won"]

    save_user_statistics(username, statistics, current_difficulty)