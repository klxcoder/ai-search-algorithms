def read_arr(path):
    arr = []
    with open(path, 'r') as file:
        for line in file:
            line = line.rstrip('\n') # removes only the trailing newline
            arr.append(list(line))
    return arr

def print_arr(arr):
    row = len(arr)
    for r in range(row):
        print(arr[r])

def find_start(arr):
    row = len(arr)
    col = len(arr[0])
    for r in range(row):
        for c in range(col):
            if arr[r][c] == "A":
                return (r, c)
    return None

def get_flags(arr):
    n_row = len(arr)
    n_col = len(arr[0])
    flags = []
    for r in range(n_row):
        row = []
        for c in range(n_col):
            row.append('0')
        flags.append(row)
    return flags

def get_adjacent_cells(cell, flags, arr):
    row = cell[0]
    col = cell[1]
    n_row = len(flags)
    n_col = len(flags[0])
    adjacent_cells = []
    for d_row, d_col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        new_row = row + d_row
        new_col = col + d_col
        if new_row in range(n_row) and new_col in range(n_col):
            if flags[new_row][new_col] == '0' and arr[new_row][new_col] != '#':
                adjacent_cells.append((new_row, new_col))
    return adjacent_cells

def find_shortest_bfs_path(arr, start):
    row = len(arr)
    col = len(arr[0])
    flags = get_flags(arr)
    frontier = [start]
    flags[start[0]][start[1]] = '1'
    cost = 0
    while len(frontier) != 0:
        first = frontier.pop(0)
        print('Will explore from ', first)
        adjacent_cells = get_adjacent_cells(first, flags, arr)
        print('adjacent_cells = ', adjacent_cells)

if __name__ == "__main__":
    arr = read_arr("src/src0/maze1.txt")
    print_arr(arr)
    start = find_start(arr)
    print(start)
    shortest_bfs_path = find_shortest_bfs_path(arr, start)
    print(shortest_bfs_path)