# Python script for solving 9x9 sudoku puzzles
# Currently only works for this size and python 3
# Example puzzles that are accepted look like:

# _ 8 _ 4 _ 7 _ 9 _
# 3 _ 4 _ _ _ 8 _ 2
# _ 6 _ _ _ _ _ 7 _
# 6 _ _ _ _ _ _ _ 1
# _ _ _ _ _ _ _ _ _
# 8 _ _ _ _ _ _ _ 9
# _ 1 _ _ _ _ _ 3 _
# 2 _ 5 _ _ _ 1 _ 7
# _ 3 _ 8 _ 9 _ 5 _

# TO RUN PROGRAM
# cd to directory containing this script
# make sure that your sudoku puzzle is the form above
# run script with "python solver.py puzzle.txt"
# Where puzzle.txt is your sudoku puzzle that you want to solve

# Some useful libraries
import csv
import sys

# global variables for puzzle properties
PUZZLE_SIZE = 9
BOX_SIZE = 3


def read_file(filename):
    """Reads a puzzle from a file.

    Args:
        param1 (str) filename: the file to be read

    Returns:
        A list of lines(list) from the file

    """

    data = []

    with open(filename) as csv_data:
        csv_reader = csv.reader(csv_data)

        for line in csv_reader:
            data.append(line[0].split())

    return data

def create_grid(data):
    """Creates a grid of 0s for unsolved spaces, and
       numbers 1-9 for already solved spaces.

    Args:
        param1 (nested list) data: the puzzle data stored

    Returns:
        A new grid with numbers instead of characters

    """

    grid = []

    # Own function created to convert a character to a number
    # Otherwise fill in a underscore '_' character
    check_char = lambda x : int(x) if x.isdigit() else 0

    for line in data:
        row = []

        for char in line:
            row.append(check_char(char))

        grid.append(row)

    return grid

def get_unsolved(grid):
    """Creates a list of tuples of all the coordinates in the grid
       that are unsolved.

    Args:
        param1 (nested list) grid: the grid representing the puzzle
    
    Returns:
        A list of tuples of all the unsolved coordinates. This is used
        for backtracking later on. 

    """

    unsolved = []

    for row in range(len(grid)):

        for col in range(len(grid[row])):

            # 0 is an unsolved space, append its coordinates
            if grid[row][col] == 0:
                unsolved.append((row, col))

    return unsolved

def valid_row(row, n):
    """Checks if a row is valid or not.

    Args:
        param1 (list) row : The row to be checked
        param2 (int) n    : The size of the row
    
    Returns:
        A boolean indicating if the row is valid or not

    """

    # If the row is not the right size, then its not valid
    if len(row) != n:
        return False

    # Get all valid spaces
    lst = [x for x in row if x > 0]

    # Checking if the row is all distinct numbers 1-9
    return len(set(lst)) == len(lst)

def valid_grid(grid, n):
    """Checks if a sudoku grid is valid

    Args:
        param1 (nested list) grid : the grid representing the puzzle
        param2 (int) n            : the size of the puzzle

    Returns:
        Returns a boolean indicating if the grid is valid or not

    """

    # First check the rows
    for row in grid:
        if not valid_row(row, n):
            return False

    # Second, transpose the rows into columns, and check it
    for row in zip(*grid):
        if not valid_row(row, n):
            return False

    # If we reach here, the puzzle is valid
    return True

def solve_puzzle(grid, unsolved, n):
    """Solves a sudoku puzzle using backtracking. The puzzle is solved
       when the unsolved puzzle has no coordinates to be solved. 

    Args:
        param1 (nested list) grid : the grid representing the puzzle
        param2 (list) unsolved    : the unsolved coordinates in the puzzle
        param3 (int) n            : the size of the puzzle

    Returns:
        Returns a solved puzzle, if possible

    """

    curr_coord = 0

    # Backtracks until no more coordinates in unsolved list are left
    while curr_coord < len(unsolved):
        row, col = unsolved[curr_coord]

        # If the grid coord reaches maximum number, reset coordinate
        if grid[row][col] == n:
            grid[row][col] = 0
            curr_coord -= 1
            continue

        grid[row][col] += 1
        if valid_grid(grid, n):
            curr_coord += 1

    return grid

def grid_output(grid, n, m):
    """Prints out the puzzle in a nice format. This could be improved.

    Args:
        param1 (nested list) grid : the grid representing the puzzle
        param2 (int) n            : the puzzle size
        param3 (int) m            : the size of each in box in the puzzle

    Returns:
        Returns a formatted string of a grid

    """

    output = ""

    # Loop over the line, and line numbers
    for num, line in enumerate(grid):

        # Prints out dashes for horizontal borders
        if num % m == 0:
            output += "- " * (n + m + 1)
            output += "\n"

        # Each line starts with a vertical border
        output += "| "

        # Converts element in the list to a string
        numbers = " ".join(map(str, line))

        # Inserts a vertical character every m characters
        numbers = "| ".join(numbers[i:i+m*2] for i in 
                            range(0, len(numbers), m*2))
        output += numbers
        output += " |\n"

    # Border for end of puzzle
    output += "- " * (n + m + 1)
    output += "\n"

    # Replaces 0s with underscores
    if "0" in output:
        output = output.replace("0", "_")

    return output

def main():
    """Main function of program. Executes python script from here.

       Args:
            None

       Returns:
            None

    """

    # If a script and a puzzle is not provided
    if len(sys.argv) < 2:
        print("Two arguements needed, the script and suduko puzzle file")
        sys.exit(1)

    # Solve each puzzle supplied
    for i in range(1, len(sys.argv)):

        # Read the sudoku puzzle
        data = read_file(sys.argv[i])
        
        # Create the grid from the data
        grid = create_grid(data)

        # If the grid is not valid, don't proceed
        if not valid_grid(grid, PUZZLE_SIZE):
            print("Invalid puzzle %d, no solution found\n" % (i))

            print("Make sure puzzle is in the form:\n")
            print("_ 8 _ 4 _ 7 _ 9 _")
            print("3 _ 4 _ _ _ 8 _ 2")
            print("_ 6 _ _ _ _ _ 7 _")
            print("6 _ _ _ _ _ _ _ 1")
            print("_ _ _ _ _ _ _ _ _")
            print("8 _ _ _ _ _ _ _ 9")
            print("_ 1 _ _ _ _ _ 3 _")
            print("2 _ 5 _ _ _ 1 _ 7")
            print("_ 3 _ 8 _ 9 _ 5 _\n")

            print("Requirements of puzzle file: ")
            print("1. Unfilled spaces with '_' character")
            print("2. Filled spaces with numbers 1 - 9")
            print("3. No repeating number in each row or column")

            sys.exit(1)

        # Original puzzle here
        print("######## PUZZLE %d #######" % (i))
        print(grid_output(grid, PUZZLE_SIZE, BOX_SIZE))

        # Get unsolved coordinates
        unsolved = get_unsolved(grid)
        
        # Solve the puzzle
        puzzle = solve_puzzle(grid, unsolved, PUZZLE_SIZE)

        # Solved puzzle here
        print("#### SOLVED PUZZLE %d ####" % (i))
        print(grid_output(puzzle, PUZZLE_SIZE, BOX_SIZE))

if __name__ == '__main__':
    main()