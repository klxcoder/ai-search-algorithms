def read_arr(path):
    arr = []
    with open(path, 'r') as file:
        for line in file:
            line = line.rstrip('\n') # removes only the trailing newline
            arr.append(line) 
    return arr

if __name__ == "__main__":
    arr = read_arr("src/src0/maze1.txt")
    print(arr)