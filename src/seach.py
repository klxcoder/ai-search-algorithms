import matplotlib.pyplot as plt
from collections import deque

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

def show_arr(arr, start, end, path):
    n_row = len(arr)
    n_col = len(arr[0])
    maze = []
    for r in range(n_row):
        row = []
        for c in range(n_col):
            if arr[r][c] == '#':
                row.append(1)
            else:
                row.append(0)
        maze.append(row)
    plt.figure(figsize=(8, 8))
    plt.imshow(maze, cmap='gray_r')

    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, color='red', linewidth=3)  # Shortest path in red

    plt.scatter([start[1], end[1]], [start[0], end[0]], c=['green', 'blue'], s=100)  # Start & end markers
    plt.axis('off')
    plt.show()

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
    row, col = cell
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

def backtrack(cell, start, back, arr):
    path = []
    save_cell = cell
    while cell != start:
        path.append(cell)
        cell = back[cell]
    path.pop(0)
    for p in path:
        arr[p[0]][p[1]] = '*'
    print_arr(arr)
    path.insert(0, save_cell)
    path.append(start)
    return path

class Node:
    def __init__(self, id, actions):
        self.id = id
        self.actions = actions
"""
class search should know nothing about arr?
search is the typical class for any search algorithm
it just find goal by expand nodes



"""
class BFS:
    def __init__(self, arr, start):
        self.arr = arr
        self.start = start

    def run(self):
        flags = get_flags(self.arr)
        frontier = deque([self.start])
        back = {}
        while len(frontier) != 0:
            # popleft -> bfs
            # pop -> dfs
            first = frontier.popleft()
            flags[first[0]][first[1]] = '1'
            if self.arr[first[0]][first[1]] == 'B':
                path = backtrack(first, self.start, back, self.arr)
                show_arr(self.arr, self.start, first, path)
                break
            adjacent_cells = get_adjacent_cells(first, flags, self.arr)
            frontier += adjacent_cells
            for cell in adjacent_cells:
                back[cell] = first


if __name__ == "__main__":
    arr = read_arr("src/src0/maze2.txt")
    print_arr(arr)
    start = find_start(arr)
    print('-'*5*len(arr[0]))
    bfs = BFS(arr, start)
    bfs.run()