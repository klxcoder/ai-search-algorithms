import matplotlib.pyplot as plt
from collections import deque
import heapq

class Frontier:
    def is_empty(self) -> bool:
        raise NotImplementedError
    def push(self, node, cost=None):
        raise NotImplementedError
    def pop(self):
        raise NotImplementedError
    
class BFSFrontier(Frontier):
    def __init__(self, start):
        self.frontier = deque([start])
    
    def is_empty(self):
        return len(self.frontier) == 0

    def push(self, node, cost=None):
        self.frontier.append(node)

    def pop(self):
        return self.frontier.popleft()

class DFSFrontier(BFSFrontier):
    def __init__(self, start):
        self.frontier = deque([start])

    def pop(self):
        return self.frontier.pop()

class AStarFrontier(Frontier):
    def __init__(self, start, start_cost=0):
        self.frontier = [(start_cost, start)]
        heapq.heapify(self.frontier)
    
    def is_empty(self):
        return len(self.frontier) == 0

    def push(self, node, cost):
        heapq.heappush(self.frontier, (cost, node))

    def pop(self):
        return heapq.heappop(self.frontier)[1]

class Search():
    def __init__(self, start, frontier):
        self.start = start
        self.frontier = frontier
        self.back = {}
        self.costs = {start: 0}  # cost from start to node
    def _mark_visited(self, node):
        raise NotImplementedError
    def _is_visited(self, node) -> bool:
        raise NotImplementedError
    def _is_goal(self) -> bool:
        raise NotImplementedError
    def _get_adjacent_nodes(self, node):
        raise NotImplementedError
    def __backtrack(self, node):
        path = []
        while node != self.start:
            path.append(node)
            node = self.back[node]
        path.append(self.start)
        return path
    def _calculate_cost(self, node, cumulative_cost):
        return 0
    def get_path(self):
        while not self.frontier.is_empty():
            node = self.frontier.pop()
            self._mark_visited(node)
            if self._is_goal(node):
                path = self.__backtrack(node)
                return path
            adjacent_nodes = self._get_adjacent_nodes(node)
            for next_node in adjacent_nodes:
                if next_node in self.costs:
                    continue
                step_cost = 1
                new_cumulative_cost = self.costs[node] + step_cost
                new_cost = self._calculate_cost(next_node, new_cumulative_cost)
                self.frontier.push(next_node, new_cost)
                self.back[next_node] = node
                self.costs[next_node] = new_cumulative_cost
        return []

class MazeSearch(Search):
    def __init__(self, start, frontier, arr, goal):
        super().__init__(start, frontier)
        self.arr = arr
        self.n_row = len(self.arr)
        self.n_col = len(self.arr[0])
        self.flags = self.__init_flags()
        self.goal = goal

    def __init_flags(self):
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
        return node == self.goal

    def _get_adjacent_nodes(self, node):
        row, col = node
        adjacent_nodes = []
        for d_row, d_col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            new_row = row + d_row
            new_col = col + d_col
            if new_row in range(self.n_row) and new_col in range(self.n_col):
                if not self._is_visited((new_row, new_col)) and self.arr[new_row][new_col] != '#':
                    adjacent_nodes.append((new_row, new_col))
        return adjacent_nodes

class GreedyMazeSearch(MazeSearch):
    def _calculate_cost(self, node, g):
        h = abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])
        return h
    
class AStarMazeSearch(MazeSearch):
    def _calculate_cost(self, node, g):
        # Use the sum of cumulative cost and heuristic
        h = abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])
        return g + h

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

def find_cell(arr, value):
    row = len(arr)
    col = len(arr[0])
    for r in range(row):
        for c in range(col):
            if arr[r][c] == value:
                return (r, c)
    return None

def show_arr_subplot(arr, start, end, path, ax, title=""):
    n_row = len(arr)
    n_col = len(arr[0])
    maze = []
    for r in range(n_row):
        row = []
        for c in range(n_col):
            row.append(1 if arr[r][c] == '#' else 0)
        maze.append(row)
    ax.imshow(maze, cmap='gray_r')

    if path:
        path_x, path_y = zip(*path)
        ax.plot(path_y, path_x, color='red', linewidth=3)  # path in red
    ax.scatter([start[1], end[1]], [start[0], end[0]], c=['green', 'blue'], s=100)
    ax.set_title(title)
    ax.axis('off')

def test_xfs(arr, start, end, search, ax, title):
    path = search.get_path()
    show_arr_subplot(arr, start, end, path, ax, title)

def test():
    arr = read_arr("src/src0/maze4.txt")
    print_arr(arr)
    start = find_cell(arr, "A")
    end = find_cell(arr, "B")

    fig, axs = plt.subplots(2, 2, figsize=(8, 8))

    test_xfs(arr, start, end, MazeSearch(start, BFSFrontier(start), arr, end), axs[0, 0], 'BFS')
    test_xfs(arr, start, end, MazeSearch(start, DFSFrontier(start), arr, end), axs[0, 1], 'DFS')
    test_xfs(arr, start, end, GreedyMazeSearch(start, AStarFrontier(start), arr, end), axs[1, 0], 'Greedy')
    test_xfs(arr, start, end, AStarMazeSearch(start, AStarFrontier(start), arr, end), axs[1, 1], 'A*')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    test()