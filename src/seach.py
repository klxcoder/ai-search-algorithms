def read_arr(path):
    arr = []
    with open(path, 'r') as file:
        for line in file:
            line = line.rstrip('\n') # removes only the trailing newline
            arr.append(line) 
    return arr

def find_start(arr):
    row = len(arr)
    col = len(arr[0])
    for r in range(row):
        for c in range(col):
            if arr[r][c] == "A":
                return (r, c)
    return None

if __name__ == "__main__":
    arr = read_arr("src/src0/maze1.txt")
    print(arr)
    start = find_start(arr)
    print(start)