import json
import random
import os
from decimal import Decimal

from matplotlib import pyplot as plt

DIR = "inputs/"
number_of_tests = len([name for name in os.listdir(DIR) if not os.path.isfile(os.path.join(DIR, name))])
current_path = os.getcwd()
destination_path = os.path.join(current_path, 'output')
if not os.path.exists(destination_path):
    os.makedirs(destination_path)

parents = {}
children = {}
all_nodes = []
CPT = {}


def topological_sort(nodes):
    l1 = len(nodes)
    res = []
    for i in range(l1):
        for node in nodes:
            if node in res:
                continue
            is_ok = True
            for k in parents[node]:
                if k not in res:
                    is_ok = False
                    break
            if is_ok:
                res.append(node)
    return res


def calculate_parents_state(node, state):
    node_state = 0
    for i in range(len(parents[node])):
        if state[parents[node][i]] == 1:
            node_state += (1 << i)
    return node_state


def calculate_probability(state):
    ans = 1
    for node in all_nodes:
        if state[node] == 1:
            ans *= CPT[node][calculate_parents_state(node, state)]
        else:
            ans *= (1 - CPT[node][calculate_parents_state(node, state)])
        # ans *= CPT[node][calculate_parents_state(node, state)]
    return ans


def is_state_consistent_with_given_states(state, given_states):
    for k in given_states.keys():
        if state[k] != given_states[k]:
            return False
    return True


def create_all_consistent_states(given_states):
    res = []
    for i in range(2 ** len(all_nodes)):
        state = {}
        for j in range(len(all_nodes)):
            if (i & (1 << j)) > 0:
                state[all_nodes[j]] = 1
            else:
                state[all_nodes[j]] = 0
        if is_state_consistent_with_given_states(state, given_states):
            res.append(state)
    return res


def inference(query):
    given_states = create_all_consistent_states(query[1])
    all_states = create_all_consistent_states({**query[1], **query[0]})
    res1 = 0
    res2 = 0
    for state in all_states:
        res1 += calculate_probability(state)
    for state in given_states:
        res2 += calculate_probability(state)
    return res1 / res2


def get_number(l):
    res = 0
    for i in range(len(l) - 1):
        if l[i] == '1':
            res += (1 << (i))
    return res


def likelihood_sample(query):
    weight = 1
    res = {}
    for node in all_nodes:
        parents_state = calculate_parents_state(node, res)
        if node in query.keys():
            if query[node] == 1:
                weight *= CPT[node][parents_state]
            else:
                weight *= (1 - CPT[node][parents_state])
            res[node] = query[node]
        x = random.uniform(0, 1)
        if x < CPT[node][parents_state]:
            res[node] = 1
        else:
            res[node] = 0
    return (res, weight)


def likelihood_sampling(query, n):
    weight_of_all_samples = 0
    weight_of_wanted_samples = 0
    for i in range(n):
        res, weight = likelihood_sample(query[1])
        weight_of_all_samples += weight
        if is_state_consistent_with_given_states(res, query[0]):
            weight_of_wanted_samples += weight
    return weight_of_wanted_samples / weight_of_all_samples


def rejection_sample(evidence):
    res = {}
    for node in all_nodes:
        parents_state = calculate_parents_state(node, res)
        x = random.uniform(0, 1)
        if x < CPT[node][parents_state]:
            res[node] = 1
        else:
            res[node] = 0
        if node in evidence:
            if res[node] != evidence[node]:
                return None
    return res


def rejection_sampling(query, n):
    number_of_accepted_samples = 0
    number_of_wanted_samples = 0
    for i in range(n):
        res = rejection_sample(query[1])
        if res is not None:
            number_of_accepted_samples += 1
            if is_state_consistent_with_given_states(res, query[0]):
                number_of_wanted_samples += 1
    if number_of_accepted_samples == 0:
        return 0
    return number_of_wanted_samples / number_of_accepted_samples


def prior_sample():
    res = {}
    for node in all_nodes:
        parents_state = calculate_parents_state(node, res)
        x = random.uniform(0, 1)
        if x < CPT[node][parents_state]:
            res[node] = 1
        else:
            res[node] = 0
    return res


def prior_sampling(query, n):
    number_of_consistent_with_evidence_samples = 0
    number_of_wanted_samples = 0
    for i in range(n):
        res = prior_sample()
        if is_state_consistent_with_given_states(res, query[1]):
            number_of_consistent_with_evidence_samples += 1
            if is_state_consistent_with_given_states(res, query[0]):
                number_of_wanted_samples += 1
    if number_of_consistent_with_evidence_samples == 0:
        return 0
    return number_of_wanted_samples / number_of_consistent_with_evidence_samples


def choose_non_evidence_node(query):
    while True:
        node = random.choice(all_nodes)
        if node not in query.keys():
            return node


def gibbs_sampling(query, n):
    number_of_wanted_samples = 0
    state, weight = likelihood_sample(query[1])
    for i in range(n):
        node = choose_non_evidence_node(query[1])
        p1 = calculate_probability(state)
        state[node] = 1 - state[node]
        p2 = calculate_probability(state)
        probability = p1 / (p1 + p2)
        x = random.uniform(0, 1)
        if x < probability:
            state[node] = 1 - state[node]
        if is_state_consistent_with_given_states(state, query[0]):
            number_of_wanted_samples += 1
    return number_of_wanted_samples / n


def solve_test(test_case):
    # print("___________________________________________")
    # print("solving test case: ", test_case)
    global all_nodes
    global CPT
    global children
    global parents
    parents = {}
    children = {}
    all_nodes = []
    CPT = {}
    prior_sampling_errors = []
    rejection_sampling_errors = []
    likelihood_sampling_errors = []
    gibbs_sampling_errors = []
    values = []
    output = open('output/' + str(test_case) + '.txt', 'w')
    input_file = open("inputs/" + str(test_case) + "/input.txt", "r")
    n = int(input_file.readline())
    for i in range(n):
        node_name = input_file.readline().strip()
        all_nodes.append(node_name)
        parents[node_name] = []
        if node_name not in children:
            children[node_name] = []
        CPT[node_name] = {}
        next_line = input_file.readline().strip().split()
        if len(next_line) == 1 and not next_line[0].isalpha():
            CPT[node_name][0] = Decimal(next_line[0])
        else:
            parents[node_name] = next_line
            for parent in parents[node_name]:
                if parent not in children.keys():
                    children[parent] = []
                children[parent].append(node_name)
            number_of_parents = len(parents[node_name])
            for j in range(2 ** number_of_parents):
                l = input_file.readline().strip().split()
                num = get_number(l)
                CPT[node_name][num] = Decimal(l[number_of_parents])
    input_file.close()
    all_nodes = topological_sort(all_nodes)
    query_file = open("inputs/" + str(test_case) + "/q_input.txt", "r")
    queries = json.loads(query_file.readline().strip())
    Xs = [x for x in range(1,len(queries)+1)]
    query_file.close()
    for query in queries:
        real_value = Decimal(inference(query))
        prior_sampling_value = Decimal(prior_sampling(query, 2000))
        likelihood_sampling_value = Decimal(likelihood_sampling(query, 2000))
        rejection_sampling_value = Decimal(rejection_sampling(query, 2000))
        gibbs_sampling_value = Decimal(gibbs_sampling(query, 2000))
        values.append(real_value)
        prior_sampling_errors.append(abs(real_value - prior_sampling_value))
        likelihood_sampling_errors.append(abs(real_value - likelihood_sampling_value))
        rejection_sampling_errors.append(abs(real_value - rejection_sampling_value))
        gibbs_sampling_errors.append(abs(real_value - gibbs_sampling_value))
        output.write(str(real_value) + " " + str(abs(real_value - prior_sampling_value)) + " " + str(
            abs(real_value - rejection_sampling_value)) + " " + str(
                abs(real_value - likelihood_sampling_value)) + " " + str(
                abs(real_value - gibbs_sampling_value))+"\n")
    output.close()
    plt.plot(Xs, values, label="real")
    plt.plot(Xs, prior_sampling_errors, label="prior sampling")
    plt.plot(Xs, rejection_sampling_errors, label="rejection sampling")
    plt.plot(Xs, likelihood_sampling_errors, label="likelihood sampling")
    plt.plot(Xs, gibbs_sampling_errors, label="gibbs sampling")
    plt.legend(loc="upper right")
    plt.savefig('output/' + str(test_case) + '.png')
    plt.show()

    # print("___________________________________________")


for i in range(1, number_of_tests + 1):
    solve_test(i)
