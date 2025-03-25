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

def find_shortest_bfs_path(arr, start):
    row = len(arr)
    col = len(arr[0])
    flags = get_flags(arr)
    frontier = [start]
    flags[start[0]][start[1]] = '1'
    cost = 0
    print_arr(flags)

if __name__ == "__main__":
    arr = read_arr("src/src0/maze1.txt")
    print_arr(arr)
    start = find_start(arr)
    print(start)
    shortest_bfs_path = find_shortest_bfs_path(arr, start)
    print(shortest_bfs_path)