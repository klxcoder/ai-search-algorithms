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
    def _is_visited(self) -> bool:
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
                step_cost = 1
                new_cumulative_cost = self.costs[node] + step_cost
                new_cost = self._calculate_cost(next_node, new_cumulative_cost)
                self.frontier.push(next_node, new_cost)
                self.back[next_node] = node
                self.costs[next_node] = new_cumulative_cost
        return []

class MazeSearch(Search):
    def __init__(self, start, frontier, arr, goal, search_type="astar"):
        super().__init__(start, frontier)
        self.arr = arr
        self.n_row = len(self.arr)
        self.n_col = len(self.arr[0])
        self.flags = self.__init_flags()
        self.goal = goal
        self.search_type = search_type

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

    # Override _calculate_cost to support Greedy and A* search
    def _calculate_cost(self, node, g):
        # Heuristic: Manhattan distance from node to goal
        h = abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])
        if self.search_type == "greedy":
            return h  # Greedy uses only the heuristic
        elif self.search_type == "astar":
            return g + h  # A* uses the sum of path cost and heuristic
        else:
            return g + h  # Default to A* if search_type is unrecognized

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

def test_xfs(start, arr, frontier, goal, search_type="astar"):
    search = MazeSearch(start, frontier, arr, goal, search_type)
    path = search.get_path()
    show_arr(arr, path)

def test():
    arr = read_arr("src/src0/maze3.txt")
    print_arr(arr)
    start = find_cell(arr, "A")
    end = find_cell(arr, "B")
    test_xfs(start, arr, BFSFrontier(start), end)
    test_xfs(start, arr, DFSFrontier(start), end)
    test_xfs(start, arr, AStarFrontier(start, 0), end, search_type="astar")
    test_xfs(start, arr, AStarFrontier(start, 0), end, search_type="greedy")

if __name__ == "__main__":
    test()