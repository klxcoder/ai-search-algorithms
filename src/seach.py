import matplotlib.pyplot as plt
from collections import deque

class Node:
    def __init__(self, id, actions):
        self.id = id
        self.actions = actions

class Frontier:
    def is_empty(self) -> bool:
        raise NotImplementedError
    def push(self, node):
        raise NotImplementedError
    def pop(self):
        raise NotImplementedError
    
class BFSFrontier(Frontier):
    def __init__(self, start):
        self.frontier = deque([start])
    
    def is_empty(self):
        return len(self.frontier) == 0

    def push(self, node):
        self.frontier.append(node)

    def pop(self):
        return self.frontier.popleft()

class DFSFrontier(Frontier):
    def __init__(self, start):
        self.frontier = deque([start])
    
    def is_empty(self):
        return len(self.frontier) == 0

    def push(self, node):
        self.frontier.append(node)

    def pop(self):
        return self.frontier.pop()

class Search():
    def _mark_visited(self, node):
        raise NotImplementedError
    def _is_visited(self) -> bool:
        raise NotImplementedError
    def _is_goal(self) -> bool:
        raise NotImplementedError
    def get_adjacent_nodes(self, node):
        raise NotImplementedError
    def __backtrack(self, node):
        path = []
        save_node = node
        while node != self.start:
            path.append(node)
            node = self.back[node]
        path.pop(0)
        path.insert(0, save_node)
        path.append(self.start)
        return path
    def get_path(self):
        while not self.frontier.is_empty():
            node = self.frontier.pop()
            self._mark_visited(node)
            if self._is_goal(node):
                path = self.__backtrack(node)
                return path
            adjacent_nodes = self.get_adjacent_nodes(node)
            for next_node in adjacent_nodes:
                self.frontier.push(next_node)
                self.back[next_node] = node

class MazeSearch(Search):
    def __init__(self, arr, start, frontier):
        self.arr = arr
        self.start = start
        self.frontier = frontier
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

    def _mark_visited(self, node):
        self.flags[node[0]][node[1]] = '1'

    def _is_visited(self, node):
        return self.flags[node[0]][node[1]] == '1'

    def _is_goal(self, node):
        return self.arr[node[0]][node[1]] == 'B'

    def get_adjacent_nodes(self, node):
        row, col = node
        adjacent_nodes = []
        for d_row, d_col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            new_row = row + d_row
            new_col = col + d_col
            if new_row in range(self.n_row) and new_col in range(self.n_col):
                if not self._is_visited((new_row, new_col)) and self.arr[new_row][new_col] != '#':
                    adjacent_nodes.append((new_row, new_col))
        return adjacent_nodes

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
    arr = read_arr("src/src0/maze3.txt")
    print_arr(arr)
    start = find_start(arr)
    frontier = DFSFrontier(start)
    bfs = MazeSearch(arr, start, frontier)
    path = bfs.get_path()
    show_arr(arr, path)

if __name__ == "__main__":
    test()