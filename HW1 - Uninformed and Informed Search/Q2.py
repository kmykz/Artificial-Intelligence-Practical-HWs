import copy

n, m = [int(x) for x in input().split()]
s = []
left = {}
right = {}
up = {}
down = {}
inf = 10 ** 12
ans = inf
x = []
t = []


def dfs(y, z):
    global ans
    if z >= ans:
        return

    if y == n * m:
        if z < ans:
            ans = z
        return
    for i in range(n):
        for j in range(m):
            if x[i][j] == -1:
                q = []
                if i != n - 1 and x[i+1][j] != -1 and x[i+1][j][0] in up:
                    for tile in up[x[i+1][j][0]]:
                        if t[tile] == 0:
                            q.append(tile)
                if j != m - 1 and x[i][j+1] != -1 and x[i][j+1][3] in left:
                    for tile in left[x[i][j+1][3]]:
                        if t[tile] == 0:
                            q.append(tile)
                if i != 0 and x[i-1][j] != -1 and x[i-1][j][2] in down:
                    for tile in down[x[i-1][j][2]]:
                        if t[tile] == 0:
                            q.append(tile)
                if j != 0 and x[i][j-1] != -1 and x[i][j-1][1] in right:
                    for tile in right[x[i][j-1][1]]:
                        if t[tile] == 0:
                            q.append(tile)
                q = list(dict.fromkeys(q))
                for tile in q:
                    minCost = inf
                    if i != n - 1 and x[i+1][j] != -1 and x[i+1][j][0] == s[tile][2]:
                        minCost = min(minCost, s[tile][2])
                    if j != m - 1 and x[i][j+1] != -1 and x[i][j+1][3] == s[tile][1]:
                        minCost = min(minCost, s[tile][1])
                    if i != 0 and x[i-1][j] != -1 and x[i-1][j][2] == s[tile][0]:
                        minCost = min(minCost, s[tile][0])
                    if j != 0 and x[i][j-1] != -1 and x[i][j-1][1] == s[tile][3]:
                        minCost = min(minCost, s[tile][3])
                    x[i][j] = s[tile]
                    t[tile] = 1
                    dfs(y+1, z+minCost)
                    x[i][j] = -1
                    t[tile] = 0


for i in range(n*m):
    a, b, c, d = [int(x) for x in input().split()]
    if not c in up:
        up[c] = []
    up[c].append(i)
    if not a in down:
        down[a] = []
    down[a].append(i)
    if not b in left:
        left[b] = []
    left[b].append(i)
    if not d in right:
        right[d] = []
    right[d].append(i)
    s.append((a, b, c, d))

s1 = [-1]*m
for a in range(n):
    x.append(s1.copy())
t = [0] * (n * m)
t[0] = 1
firstTile = s[0]


for i in range(n):
    for j in range(m):
        x[i][j] = firstTile
        dfs(1, 0)
        x[i][j] = -1
print(ans)
