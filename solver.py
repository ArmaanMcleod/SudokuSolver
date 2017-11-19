import csv
import sys

PUZZLE_SIZE = 9
BOX_SIZE = 3

def read_file(filename):
    data = []

    with open(filename) as csv_data:
        csv_reader = csv.reader(csv_data)

        for line in csv_reader:
            data.append(line[0].split())

    return data


def create_grid(data):
    grid = []

    check_char = lambda x : int(x) if x.isdigit() else 0

    for line in data:
        row = []

        for char in line:
            row.append(check_char(char))

        grid.append(row)

    return grid

def get_unsolved(grid):
    unsolved = []

    for row in range(len(grid)):

        for col in range(len(grid[row])):

            if grid[row][col] == 0:
                unsolved.append((row, col))

    return unsolved

def valid_row(row, n):
    if len(row) != n:
        return False

    lst = [x for x in row if x > 0]

    return len(set(lst)) == len(lst)

def valid_grid(grid, n):
    for row in grid:
        if not valid_row(row, n):
            return False

    for row in zip(*grid):
        if not valid_row(row, n):
            return False

    return True

def solve_puzzle(grid, unsolved, n):
    curr_coord = 0

    while curr_coord < len(unsolved):
        row, col = unsolved[curr_coord]

        if grid[row][col] == n:
            grid[row][col] = 0
            curr_coord -= 1
            continue


        grid[row][col] += 1
        if valid_grid(grid, n):
            curr_coord += 1

    return grid

def grid_output(grid, n, m):
    output = ""

    for num, line in enumerate(grid):
        if num % m == 0:
            output += "- " * (n + m + 1)
            output += "\n"

        output += "| "
        numbers = " ".join(map(str, line))
        numbers = "| ".join(numbers[i:i+m*2] for i in 
                            range(0, len(numbers), m*2))
        output += numbers
        output += " |\n"

    output += "- " * (n + m + 1)
    output += "\n"

    return output

def main():
    if len(sys.argv) != 2:
        print("Two arguements needed, the script and suduko puzzle file")
        sys.exit(1)

    data = read_file(sys.argv[1])
    
    grid = create_grid(data)

    if not valid_grid(grid, PUZZLE_SIZE):
        print("Invalid puzzle, no solution found\n")

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

    print("#### ORIGINAL PUZZLE ####")
    print(grid_output(grid, PUZZLE_SIZE, BOX_SIZE))

    unsolved = get_unsolved(grid)
    
    puzzle = solve_puzzle(grid, unsolved, PUZZLE_SIZE)

    print("##### SOLVED PUZZLE #####")
    print(grid_output(puzzle, PUZZLE_SIZE, BOX_SIZE))

if __name__ == '__main__':
    main()