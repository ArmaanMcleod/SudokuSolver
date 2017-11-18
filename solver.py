import csv
import sys

def read_file(filename):
    data = []

    with open(filename) as csv_data:
        csv_reader = csv.reader(csv_data)
        for line in csv_reader:
            data.append(line[0].split())

    return data

def create_grid(data):
    return [[int(x) if x != '_' else 0 for x in row] for row in data]

def main():

    if len(sys.argv) != 2:
        print("Two arguements needed, the script and suduko puzzle file")
        sys.exit(1)

    data = read_file(sys.argv[1])
    
    grid = create_grid(data)
    print(grid)

if __name__ == '__main__':
    main()