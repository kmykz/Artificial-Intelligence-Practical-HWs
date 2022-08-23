from decimal import Decimal
import statistics
import numpy as np

OLY_coordinates = (-133, 18)
ARS_coordinates = (-121, -9)
PAV_coordinates = (-113, 1)
ASC_coordinates = (-104, 12)
dist1 = statistics.NormalDist(2, 1)
OLY_dists = []
ARS_dists = []
PAV_dists = []
ASC_dists = []


def update_particles(parts):
    delta_x = np.random.normal(2, 1, len(parts))
    delta_y = np.random.normal(1, 1, len(parts))
    new_parts = [(p[0] + delta_x[i], p[1] + delta_y[i]) for i, p in enumerate(parts)]
    return new_parts


def calc(x, y):
    return 1 - dist1.cdf(abs(float(Decimal(x) - y)))


def calculate_weights(parts, level):
    W = []
    for p in parts:
        distance1 = np.sqrt((p[0] - OLY_coordinates[0]) ** 2 + (p[1] - OLY_coordinates[1]) ** 2)
        distance2 = np.sqrt((p[0] - ARS_coordinates[0]) ** 2 + (p[1] - ARS_coordinates[1]) ** 2)
        distance3 = np.sqrt((p[0] - PAV_coordinates[0]) ** 2 + (p[1] - PAV_coordinates[1]) ** 2)
        distance4 = np.sqrt((p[0] - ASC_coordinates[0]) ** 2 + (p[1] - ASC_coordinates[1]) ** 2)
        W.append(calc(distance1, OLY_dists[level]) * calc(distance2, ARS_dists[level]) * calc(distance3,
                                                                                              PAV_dists[level]) * calc(
            distance4, ASC_dists[level]))
    sum_of_weights = sum(W)
    W = [w / sum_of_weights for w in W]
    return W


input()
for i in range(20):
    OLY_dists.append(Decimal(input()))
input()
for i in range(20):
    ARS_dists.append(Decimal(input()))
input()
for i in range(20):
    PAV_dists.append(Decimal(input()))
input()
for i in range(20):
    ASC_dists.append(Decimal(input()))
# print(OLY_dists,"\n",ARS_dists,"\n",PAV_dists,"\n",ASC_dists)
particles_X = np.random.uniform(-170, -90, 2000)
particles_Y = np.random.uniform(-20, 40, 2000)
particles = [(x, y) for x, y in zip(particles_X, particles_Y)]
for i in range(20):
    particles = update_particles(particles)
    weights = calculate_weights(particles, i)
    weight_median = statistics.median(weights)
    to_be_remove_indexes = []
    # print("medium: ", weight_median)
    # print("mean before", statistics.mean(weights))
    for j in range(len(weights) - 1, -1, -1):
        if weights[j] < weight_median:
            to_be_remove_indexes.append(j)
    for index in to_be_remove_indexes:
        particles.pop(index)
        weights.pop(index)
    # print("mean after", statistics.mean(weights))

    weights = [w / sum(weights) for w in weights]
    indexes = [i for i in range(len(particles))]
    indexes = np.random.choice(indexes, 2000, p=weights)
    # print(np.shape(particles), np.shape(indexes), np.shape(weights))
    particles = [particles[i] for i in indexes]
    if i == 19:
        final_X = 0
        final_Y = 0
        weight_sum = 0
        for index in indexes:
            final_X += particles[index][0] * weights[index]
            final_Y += particles[index][1] * weights[index]
            weight_sum += weights[index]
        # print(weight_sum)
        final_X = final_X / weight_sum
        final_Y = final_Y / weight_sum

# print(final_X, final_Y)
print(int(np.ceil(final_X / 10) * 10))
print(int(np.ceil(final_Y / 10) * 10))
