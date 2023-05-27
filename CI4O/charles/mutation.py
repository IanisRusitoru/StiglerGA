from random import randint, sample
import random


def scramble_mutation_crp(individual, p=1):
    """Swap mutation for a GA individual. Swaps the items.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mutated_individual = list(individual)  # Create a copy of the individual
    mut_indexes = random.sample(range(0, len(mutated_individual)), 2)

    # Swap the values at the mutation indexes
    mutated_individual[mut_indexes[0]], mutated_individual[mut_indexes[1]] = mutated_individual[mut_indexes[1]], \
    mutated_individual[mut_indexes[0]]

    for i in range(len(mutated_individual)):
        if mutated_individual[i] == 0:
            mutated_individual[i] += 1
        elif random.random() < p:
            #Apply the same mutation operators and values as in the original function
            mutated_individual[i] *= random.uniform(.9, 1.1)
    return mutated_individual

def controlled_random_perturbation(individual, p=1):
    mutated_individual = list(individual)
    for i in range(len(mutated_individual)):
        # If it is 0 due to initialization we increase to 1
        if mutated_individual[i] == 0:
            mutated_individual[i] += 1
        # We added the p just to be able to tweak if all bits get mutated or not
        # We usually we use p = 1 as mentioned in the report
        # If bit =/= 0, then bit is multiplied with a random number within the random uniform range
        # The goal is to increment/decrement the bit as necessary for the algorithm
        elif random.random() < p:
        # Best for generalization for pareto foods
            mutated_individual[i] *= random.uniform(.9, 1.1)
        # When you know the foods you might want to make smaller steps
            # mutated_individual[i] *= random.uniform(.999, 1.001)

    return mutated_individual

def inversion_mutation_crp(individual, p=1):
    mutated_individual = list(individual)
    # Choose two random positions within the individual's genotype
    pos1 = random.randint(0, len(mutated_individual) - 1)
    pos2 = random.randint(0, len(mutated_individual) - 1)
    # Ensure pos1 is smaller than pos2
    pos1, pos2 = min(pos1, pos2), max(pos1, pos2)
    # Invert the subsequence between pos1 and pos2
    mutated_individual[pos1:pos2 + 1] = mutated_individual[pos1:pos2 + 1][::-1]
    for i in range(len(mutated_individual)):
        if mutated_individual[i] == 0:
            mutated_individual[i] += 1
        elif random.random() < p:
            mutated_individual[i] *= random.uniform(.9, 1.1)
    return mutated_individual

if __name__ == '__main__':
    test = [1, 2, 3, 4, 5, 6]
    test = controlled_random_perturbation(test)
    print(test)



