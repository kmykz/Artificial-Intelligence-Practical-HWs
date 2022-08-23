map = []
block = []
row = []
column = []
number_of_present_values = 0


def valid(x, y, value):
    block_X = x // 3
    block_Y = y // 3
    return row[x][value - 1] == False and column[y][value - 1] == False and block[block_X * 3 + block_Y][value - 1] == False


def valid_values(i, j):
    block_X = i // 3
    block_Y = j // 3
    cnt = 0
    for x in range(1, 10):
        if valid(i, j, x):
            cnt += 1
    return cnt


def get_value(x, y):
    for i in range(1, 10):
        if valid(x, y, i):
            return i


def get_next_best():
    global number_of_present_values
    current_best = 1000
    current_ans = (9, 9)
    for i in range(9):
        for j in range(9):
            if map[i][j] == 0:
                t = valid_values(i, j)
                if t < current_best:
                    current_best = t
                    current_ans = (i, j)
    return current_ans


def backtracking():
    global number_of_present_values
    if number_of_present_values == 81:
        return True
    x, y = get_next_best()
    block_X = x // 3
    block_Y = y // 3
    for i in range(1, 10):
        if valid(x, y, i):
            map[x][y] = i
            row[x][i - 1] = True
            column[y][i - 1] = True
            block[block_X * 3 + block_Y][i - 1] = True
            number_of_present_values += 1
            if backtracking():
                return True
            number_of_present_values -= 1
            row[x][i - 1] = False
            column[y][i - 1] = False
            block[block_X * 3 + block_Y][i - 1] = False
            map[x][y] = 0


for i in range(9):
    map.append(input().split())
    block.append([])
    block[i] = [False] * 9
    row.append([])
    row[i] = [False] * 9
    column.append([])
    column[i] = [False] * 9

for i in range(9):
    for j in range(9):
        if map[i][j] == '.':
            map[i][j] = 0
        else:
            map[i][j] = int(map[i][j])
            number_of_present_values += 1
            block_X = i // 3
            block_Y = j // 3
            block[block_X * 3 + block_Y][map[i][j] - 1] = True
            row[i][map[i][j] - 1] = True
            column[j][map[i][j] - 1] = True
backtracking()
for i in range(9):
    for j in range(9):
        print(map[i][j], end=' ')
    print()
