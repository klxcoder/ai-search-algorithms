class Node:
    def __init__(self, id, parent=None, actions = []):
        self.id = id # The identifier for the current node
        self.parent = parent # Reference to the node that transitioned to the current node
        self.actions = actions # Store actions that can be take from the current node

class Search:
    def __init__(self):
        self.frontier = [] # stores the nodes will be expored in the future
    def start(self):
        pass
        
if __name__ == "__main__":
   search = Search()
   search.start()