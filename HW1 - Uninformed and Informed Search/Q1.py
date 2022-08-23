

from heapq import heappop, heappush


inf = 10 ** 10


def solve():
    n, m = [int(x) for x in input().split()]

    badMenDists = [inf] * (n + 1)
    tintinDists = [inf] * (n + 1)
    adjs = []
    prev = [0] * (n + 1)
    for j in range(n+1):
        adjs.append([])

    for j in range(m):
        a, b, c = [int(x) for x in input().split()]
        adjs[a].append((b, c))
        adjs[b].append((a, c))
    T = input()
    badMen = list(map(int, input().split()))
    C = input()
    cars = list(map(int, input().split()))
    s, g = [int(x) for x in input().split()]
    pq = []

    for x in badMen:
        badMenDists[x] = 0
        heappush(pq, (0, x))
    while len(pq) > 0:
        a, b = heappop(pq)
        for c, d in adjs[b]:
            if(badMenDists[c] > badMenDists[b] + d):
                badMenDists[c] = badMenDists[b] + d
                heappush(pq, (badMenDists[c], c))
    for x in cars:
        heappush(pq, (badMenDists[x], x))
    while len(pq) > 0:
        a, b = heappop(pq)
        for c, d in adjs[b]:
            if(badMenDists[c] > badMenDists[b] + d/2):
                badMenDists[c] = badMenDists[b] + d/2
                heappush(pq, (badMenDists[c], c))
    tintinDists[s] = 0
    heappush(pq, (0, s))
    while len(pq) > 0:
        a, b = heappop(pq)
        for c, d in adjs[b]:
            if(tintinDists[c] > tintinDists[b] + d):
                tintinDists[c] = tintinDists[b] + d
                heappush(pq, (tintinDists[c], c))
                prev[c] = b
    if tintinDists[g] > badMenDists[g]:
        print("Poor Tintin")
        return
    print(tintinDists[g])
    res = []
    cur = g
    while cur != s:
        res.append(cur)
        cur = prev[cur]
    res.append(s)
    res.reverse()
    print(len(res))
    print(*res)


k = int(input())
for i in range(k):
    solve()
