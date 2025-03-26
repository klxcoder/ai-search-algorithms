import matplotlib.pyplot as plt
from collections import deque

class Node:
    def __init__(self, id, actions):
        self.id = id
        self.actions = actions
"""
class search should know nothing about arr?
search is the typical class for any search algorithm
it just find goal by expand nodes

class BFS implement typical BFS
    start from initial node
    and expand nodes by taking actions
    and visit unvisited node
    end when find goal

bfs will use queue (deque with popleft)

"""
class BFS:
    def __init__(self, arr, start):
        self.arr = arr
        self.start = start
        self.frontier = deque([self.start])
        self.back = {}
        self.n_row = len(self.arr)
        self.n_col = len(self.arr[0])
        self.flags = self.get_flags()

    def get_flags(self):
        flags = []
        for r in range(self.n_row):
            row = []
            for c in range(self.n_col):
                row.append('0')
            flags.append(row)
        return flags

    def backtrack(self, cell):
        path = []
        save_cell = cell
        while cell != self.start:
            path.append(cell)
            cell = self.back[cell]
        path.pop(0)
        path.insert(0, save_cell)
        path.append(self.start)
        return path

    def markVisited(self, cell):
        self.flags[cell[0]][cell[1]] = '1'

    def isVisited(self, cell):
        return self.flags[cell[0]][cell[1]] == '1'

    def isGoal(self, cell):
        return self.arr[cell[0]][cell[1]] == 'B'

    def get_adjacent_cells(self, cell):
        row, col = cell
        adjacent_cells = []
        for d_row, d_col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            new_row = row + d_row
            new_col = col + d_col
            if new_row in range(self.n_row) and new_col in range(self.n_col):
                if not self.isVisited((new_row, new_col)) and self.arr[new_row][new_col] != '#':
                    adjacent_cells.append((new_row, new_col))
        return adjacent_cells

    def get_path(self):
        while len(self.frontier) != 0:
            # popleft -> bfs
            # pop -> dfs
            cell = self.frontier.popleft()
            self.markVisited(cell)
            if self.isGoal(cell):
                path = self.backtrack(cell)
                return path
            adjacent_cells = self.get_adjacent_cells(cell)
            self.frontier += adjacent_cells
            for next_cell in adjacent_cells:
                self.back[next_cell] = cell

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

def show_arr(arr, path):
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

    end = path[0]
    start = path[-1]

    plt.scatter([start[1], end[1]], [start[0], end[0]], c=['green', 'blue'], s=100)  # Start & end markers
    plt.axis('off')
    plt.show()

def test():
    arr = read_arr("src/src0/maze2.txt")
    print_arr(arr)
    start = find_start(arr)
    bfs = BFS(arr, start)
    path = bfs.get_path()
    show_arr(arr, path)

if __name__ == "__main__":
    test()