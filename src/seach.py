def read_arr(path):
    arr = []
    with open(path, 'r') as file:
        for line in file:
            arr.append(line.strip()) # `.strip()` removes leading/trailing spaces and newlines
    return arr

if __name__ == "__main__":
    arr = read_arr("src/src0/maze1.txt")
    print(arr)