import random


def two_point_crossover(parent1, parent2):
    length = len(parent1)

    if length < 3:
        return parent1[:], parent2[:]

    point1 = random.randint(1, length - 2)
    point2 = random.randint(point1 + 1, length - 1)

    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

    return child1, child2


def uniform_crossover(parent1, parent2, crossover_probability=0.5):
    child1 = []
    child2 = []

    for i in range(len(parent1)):
        if random.random() < crossover_probability:
            child1.append(parent2[i])
            child2.append(parent1[i])
        else:
            child1.append(parent1[i])
            child2.append(parent2[i])

    return child1, child2
