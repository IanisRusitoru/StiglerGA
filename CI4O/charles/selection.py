from random import uniform, choice, sample
from operator import attrgetter
import random

def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":

        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    # Our implementation of min
    elif population.optim == "min":
    # Invert fitness values
        inverted_fitness = [max([i.fitness for i in population]) - i.fitness for i in population]
        # Sum total inverted fitness
        total_fitness = sum(inverted_fitness)
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual, inverted_fitness_value in zip(population, inverted_fitness):
            position += inverted_fitness_value
            if position > spin:
                return individual
    else:
        raise Exception("No optimization specified (min or max).")

def tournament_sel(population, size=2):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: The best individual in the tournament.
    """

    # Select individuals based on tournament size
    # with choice, there is a possibility of repetition in the choices,
    # so every individual has a chance of getting selected
    tournament = [choice(population.individuals) for _ in range(size)]

    # with sample, there is no repetition of choices
    # tournament = sample(population.individuals, size)
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    if population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))


def ranking_selection(population):
    """Ranking selection implementation for both maximization and minimization problems.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    # Check the optimization type of the population
    if population.optim == "max":
        # If maximizing, sort the population based on fitness in descending order
        sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
    elif population.optim == "min":
        # If minimizing, sort the population based on fitness in ascending order
        sorted_population = sorted(population, key=lambda x: x.fitness, reverse=False)
    else:
        raise ValueError("Invalid optimization type. Must be either 'max' or 'min'.")

    # Calculate the total ranks for selection probability calculation
    total_ranks = sum(range(1, len(sorted_population) + 1))
    # Calculate the selection probabilities for each individual
    selection_probs = [(len(sorted_population) - i + 1) / total_ranks for i in range(1, len(sorted_population) + 1)]
    spin = random.uniform(0, 1)
    position = 0

    for i, individual in enumerate(sorted_population):
        # Update the position counter based on the selection probability
        position += selection_probs[i]

        # If the position exceeds the spin value, return the current individual
        if position > spin:
            return individual
