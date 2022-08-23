from decimal import Decimal

n = int(input())
undirected_adj = [[] for i in range(n + 1)]
adj = [[] for i in range(n + 1)]
is_independent = True
observed = []


def get_direction(node1, node2):
    return node2 in adj[node1]


def has_visited_descendents(x):
    if x in observed:
        return True
    for v in adj[x]:
        if v in observed:
            return True
    return False

def is_d_separated(x, y):
    route_nodes = [(x, 1)]
    visited_nodes = []
    while len(route_nodes) > 0:
        node, direction = route_nodes.pop()
        # print(node, direction)
        if (node, direction) not in visited_nodes:
            visited_nodes.append((node, direction))
            if node == y and node not in observed:
                return False
            if direction == 1 and node not in observed:
                for u in undirected_adj[node]:
                    if get_direction(node, u):
                        route_nodes.append((u, 0))
                    else:
                        route_nodes.append((u, 1))
            elif direction == 0:
                if node not in observed:
                    for u in adj[node]:
                        route_nodes.append((u, 0))
                if has_visited_descendents(node):
                    for u in parents[node]:
                        route_nodes.append((u, 1))
    return True


parents = [[] for i in range(n + 1)]
CPT = [[] for i in range(n + 1)]
for i in range(1, n + 1):
    parents[i] = [int(x) for x in input().split()]
    CPT[i] = [Decimal(x) for x in input().split()]
lst = input().split(',')
givens = []
if lst[0] != '':
    givens = [(int(x[0]), int(x[1])) for x in [y.split('->') for y in lst]]
observed = [t[0] for t in givens]
not_observed = [x for x in range(1, n + 1) if x not in observed]
for i in range(1, n + 1):
    for j in range(len(parents[i])):
        undirected_adj[parents[i][j]].append(i)
        undirected_adj[i].append(parents[i][j])
        adj[parents[i][j]].append(i)
u, v = map(int, input().split())
# print("parents", parents)
if is_d_separated(u, v):
    print('independent')
else:
    print('dependent')
t = len(not_observed) - 1


def calculate_probability(state):
    # print(state,bin(state).replace('0b', ''))
    res = 1
    for i in range(1, n + 1):
        new_state = 0
        L = len(parents[i])
        for j in range(L):
            if ((1 << parents[i][j]) & state) == 0:
                new_state |= 1 << (L - 1 - j)
        if (1 << i) & state == 0:
            # print(1-CPT[i][new_state])
            res *= (1 - CPT[i][new_state])
        else:
            # print(CPT[i][new_state])
            res *= CPT[i][new_state]
    # print("finished",res)
    return res


def sum_on_not_observed():
    val = 0
    for i in range(2 ** t):
        val1 = 0
        for j in range(t):
            if ((1 << j) & i) != 0:
                val1 = (val1 | (1 << not_observed[j]))
        for j in range(len(givens)):
            if givens[j][1] == 1:
                val1 = (val1 | (1 << givens[j][0]))
        val = val + calculate_probability(val1)
    return val


not_observed.remove(u)
observed.append(u)
givens.append((u, 1))
u_value_true = sum_on_not_observed()
givens.pop()
givens.append((u, 0))
u_value_false = sum_on_not_observed()
print(u_value_true / (u_value_true + u_value_false))
givens.pop()
observed.pop()
not_observed.append(u)
not_observed.remove(v)
observed.append(v)
givens.append((v, 1))
v_value_true = sum_on_not_observed()
givens.pop()
givens.append((v, 0))
v_value_false = sum_on_not_observed()
print(v_value_true / (v_value_true + v_value_false))
