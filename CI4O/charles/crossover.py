from random import randint, uniform
import random

def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_point = randint(1, len(p1)-2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2

def arithmetic_xo(p1, p2):
    """Implementation of arithmetic crossover/geometric crossover with constant alpha.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    alpha = uniform(0, 1)
    o1 = [None] * len(p1)
    o2 = [None] * len(p1)
    for i in range(len(p1)):
        o1[i] = p1[i] * alpha + (1-alpha) * p2[i]
        o2[i] = p2[i] * alpha + (1-alpha) * p1[i]
    return o1, o2

def pmxo(parent1, parent2):
    size = len(parent1)
    child1 = [None] * size
    child2 = [None] * size
    start_pos = random.randint(0, size - 1)
    end_pos = random.randint(0, size - 1)

    if start_pos > end_pos:
        start_pos, end_pos = end_pos, start_pos

    # Copy the segment between start and end positions from parent1 to child1 and from parent2 to child2
    child1[start_pos:end_pos + 1] = parent1[start_pos:end_pos + 1]
    child2[start_pos:end_pos + 1] = parent2[start_pos:end_pos + 1]

    # Map the segment in parent2 to the corresponding positions in child1
    for i in range(start_pos, end_pos + 1):
        if parent2[i] not in child1:
            while child1[i] is None:
                i = parent2.index(parent1[i])
            child1[i] = parent2[i]

    # Map the segment in parent1 to the corresponding positions in child2
    for i in range(start_pos, end_pos + 1):
        if parent1[i] not in child2:
            while child2[i] is None:
                i = parent1.index(parent2[i])
            child2[i] = parent1[i]

    # Copy the remaining elements from parent2 to child1 and from parent1 to child2
    for i in range(size):
        if child1[i] is None:
            child1[i] = parent2[i]
        if child2[i] is None:
            child2[i] = parent1[i]

    return child1, child2

