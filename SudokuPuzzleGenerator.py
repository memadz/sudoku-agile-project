import random

def create_board():
    # Initialize a 9x9 grid
    grid = []

    # Fill the grids with zeros
    for i in range(9):
        lst = []

        for j in range(9):
            lst.append(0) # Append a zero to represent an empty cell

        grid.append(lst) # Add the row to the grid

    return grid # Return the initialized empty grid

def is_valid(grid, row, col, num):
    # Check if num is not in the current row
    for i in range(9):
        
        if grid[row][i] == num:
            return False # Return False if the number already exists in the row
        
    # Check if num is not in the current column
    for i in range(9):

        if grid[i][col] == num:
            return False # Return False if the number already exists in the column
        
    # Check if num is not in the current 3x3 subgrid
    subgrid_row = 3 * (row // 3) # This floor division calculates which 3x3 block the current row belongs to
    subgrid_col = 3 * (col // 3) # Similarily, this floor division calculates which 3x3 block the current column belongs to

    # The range is defined from 'subgrid_row' to 'subgrid_row + 3' which specifies the three rows that make up the current 3x3 block
    for i in range(subgrid_row, subgrid_row + 3):
        
        # The range is defined from 'subgrid_col' to 'subgrid_col + 3' which specifies the three columns that make up the current 3x3 block
        for j in range(subgrid_col, subgrid_col + 3): 
            
            # Check if the number "num" is present in the current cell of the 3x3 subgrid
            if grid[i][j] == num:
                return False # Return False if the number already exists in the 3x3 subgrid

    return True # Return True only if the number is valid for that cell

def find_empty_cell(grid):
    # Find an empty cell (0) in the grid
    for i in range(9):

        for j in range(9):

            if grid[i][j] == 0:
                return (i, j) # Return the row and column of the empty cell

    return None # No empty cells found

def generate_random_numbers():
    # Create a list of all numbers from 1-9 and shuffle it for random order
    numbers = list(range(1,10))
    random.shuffle(numbers)
    return numbers

def solve_sudoku(grid):
    empty = find_empty_cell(grid) # Find an empty cell
    if not empty:
        return True # Return True if the puzzle is solved
    
    # Unpack the tuple retrieved from the function find_empty_cell function
    row, col = empty # Assign the first element of the tuple to "row" and the second element to "col"
    numbers = generate_random_numbers() # Generate new random numbers

    for num in numbers: # Try numbers in random order

        if is_valid(grid, row, col, num): # Check if placing the number is valid
            grid[row][col] = num # Place the number in the cell

            if solve_sudoku(grid): # Recursively call the function itself til the Sudoku puzzle is solved
                return True # Return True if the puzzle is solved
            
            grid[row][col] = 0 # Backtrack if placing the number did not lead to a solution
             
    return False # Return False to trigger backtracking if no number of the randomized list is valid // Return control flow to the previous call of solve_sudoku function


def count_solutions(grid):
    empty = find_empty_cell(grid)
    if not empty:
        return 1  # Found a solution
    
    row, col = empty
    count = 0
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            count += count_solutions(grid)
            grid[row][col] = 0
            if count > 1:  # Early exit if more than one solution is found
                break

    return count

def remove_numbers(grid, clues_to_remove):
    attempts = 0

    while attempts < clues_to_remove:
        row = random.randint(0,8)
        col = random.randint(0,8)

        if grid[row][col] != 0:  # Only remove if the cell is filled
            saved_value = grid[row][col]  # Save the value to restore later
            grid[row][col] = 0  # Remove the number

            # Check if the grid still has a unique solution
            if count_solutions(grid) != 1:
                grid[row][col] = saved_value  # Restore the value if not unique
            else:
                attempts += 1  # Successfully removed a number
        
def generate_sudoku_puzzle(difficulty):
    # Create two boards: one for the puzzle (with missing numbers) and one for the solved version.
    puzzle_grid = create_board() # This board will contain the Sudoku puzzle with hidden numbers.
    solved_grid = create_board() # This board will contain the fully solved Sudoku puzzle.
    
    solve_sudoku(solved_grid) # Solve the Sudoku grid

    # Copy each element from the solved grid to the puzzle grid
    for i in range(9):
        for j in range(9):
            puzzle_grid[i][j] = solved_grid[i][j]

    TOTAL_CLUES = 81 # A 9x9 Sudoku grid has inherently 81 cells, which each when filled, is called a clue

    # Amount of clues per difficulties (Made up values for now)
    # Easy = 38 clues
    # Normal = 34 clues
    # Hard = 30 clues
    difficulty_levels = {
        "easy": TOTAL_CLUES - 38,
        "medium": TOTAL_CLUES - 34,
        "hard": TOTAL_CLUES - 30
    }

    clues_to_remove = difficulty_levels.get(difficulty)

    remove_numbers(puzzle_grid, clues_to_remove)

    return puzzle_grid, solved_grid # Return the puzzle and the fully solved grid.

def main():
    print("Hello, world?")
if __name__ == "__main__":
    main() 