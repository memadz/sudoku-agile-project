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

    return True # Return True only when the number is valid for that cell (when all the conditional statement is not met)

def find_empty_cell(grid):
    # Find an empty cell (0) in the grid
    for i in range(len(grid)):

        for j in range(len(grid)):

            if grid[i][j] == 0:
                return (i, j) # Return the row and column of the empty cell

    return None # No empty cells found

def solve_sudoku(grid):
    empty = find_empty_cell(grid) # Find an empty cell
    if not empty:
        return True # Return True if the puzzle is solved
    
    # Unpack the tuple retrieved from the function find_empty_cell function
    row, col = empty # Assign the first element of the tuple to "row" and the second element to "col"

    # Create a list of all numbers from 1-9 and shuffle it for random order
    numbers = []
    for i in range(1,10):
        numbers.append(i)
    random.shuffle(numbers)  # The shuffle function will randomize the order of the numbers in the list

    for num in numbers: # Try numbers in random order

        if is_valid(grid, row, col, num): # Check if placing the number is valid
            grid[row][col] = num # Place the number in the cell

            if solve_sudoku(grid): # Recursively call the function itself til the Sudoku puzzle is solved
                return True # Return True if the puzzle is solved
            
            grid[row][col] = 0 # Backtrack if placing the number did not lead to a solution

    return False # Return False to trigger backtracking if no number of the randomized list is valid
    
def main():
    sudoku_grid = create_board() # Create an empty Sudoku grid (9x9 grid filled with zeros)
    solve_sudoku(sudoku_grid) # Solve the Sudoku grid
    
    # We dont want to print it for the GUI
    # Print the resulting Sudoku grid
    #for row in sudoku_grid:
    #    print(row)

    return sudoku_grid

if __name__ == "__main__":
    main()