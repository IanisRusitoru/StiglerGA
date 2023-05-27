from charles.charles import Population, Individual
from charles.selection import fps, tournament_sel, ranking_selection
from charles.mutation import controlled_random_perturbation, scramble_mutation_crp, inversion_mutation_crp
from charles.crossover import single_point_co, pmxo, arithmetic_xo
from data.data import goal, foods, price, food_names, nutrient_names
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate


# Define the fitness function for the Individual class
def get_fitness(self):
    fitness = 0
    current_nutrients = [0] * len(goal)
    for bit in range(len(self.representation)):
        # multiply price by amount
        fitness += price[bit] * self.representation[bit]
        for i in range(len(current_nutrients)):
            # multiply nutrients by amount
            current_nutrients[i] += (foods[bit][i] * self.representation[bit])
    for i in range(len(current_nutrients)):
        # penalize if goals are not met
        if current_nutrients[i] < goal[i]:
            fitness -= current_nutrients[i] - goal[i]
    return fitness


# Monkey patch
Individual.get_fitness = get_fitness

# Define the selection, mutation, and crossover methods
selection = [tournament_sel]
mutation = [controlled_random_perturbation, inversion_mutation_crp, scramble_mutation_crp]
crossover = [pmxo, single_point_co, arithmetic_xo]

# Create a mapping dictionary to store combinations of selection, mutation, and crossover methods
mapping_dict = {
    (0, 0, 0): [selection[0].__name__, mutation[0].__name__, crossover[0].__name__],
    (0, 0, 1): [selection[0].__name__, mutation[0].__name__, crossover[1].__name__],
    (0, 0, 2): [selection[0].__name__, mutation[0].__name__, crossover[2].__name__],
    (0, 1, 0): [selection[0].__name__, mutation[1].__name__, crossover[0].__name__],
    (0, 1, 1): [selection[0].__name__, mutation[1].__name__, crossover[1].__name__],
    (0, 1, 2): [selection[0].__name__, mutation[1].__name__, crossover[2].__name__],
    (0, 2, 0): [selection[0].__name__, mutation[2].__name__, crossover[0].__name__],
    (0, 2, 1): [selection[0].__name__, mutation[2].__name__, crossover[1].__name__],
    (0, 2, 2): [selection[0].__name__, mutation[2].__name__, crossover[2].__name__]
}

# Create an empty list and dictionary to store results
gens = {}


# Define the function to evaluate hyperparameters
def evaluate_hyperparams(selection_methods, mutation_methods, crossover_methods, runs):
    best_fitness = float('inf')
    best_representation = None
    best_selection = None
    best_mutation = None
    best_crossover = None

    # Run the evaluation for the specified number of runs
    for i in range(runs):
        print("----------- RUN Nº", i + 1, "-----------")
        for selection in range(len(selection_methods)):
            for mutation in range(len(mutation_methods)):
                for crossover in range(len(crossover_methods)):

                    print("|| Selection:", selection, "|| Mutation:", mutation, "|| Crossover", crossover, "||")
                    # Perform evaluation for current hyperparameters
                    pop = Population(size=100, optim="min", sol_size=len(price), valid_set=range(0, 50),
                                     replacement=True)

                    gen = pop.evolve(gens=1000, xo_prob=.8, mut_prob=.95, select=selection_methods[selection],
                                     mutate=mutation_methods[mutation], crossover=crossover_methods[crossover],
                                     elitism=True)

                    # Store the gen with corresponding hyperparameters
                    key = tuple([item.fitness for item in gen])
                    value = tuple([selection, mutation, crossover])
                    if key in gens:
                        gens[key].append(value)
                    else:
                        gens[key] = value

                    # Iterate over all individuals in the population
                    for individual in gen:
                        # Check if current individual has better fitness than the previous best
                        if individual.fitness < best_fitness:
                            best_fitness = individual.fitness
                            best_selection = selection
                            best_mutation = mutation
                            best_crossover = crossover
                            best_representation = individual.representation

    result = {}
    value_set = set(map(tuple, gens.values()))

    for value in value_set:
        filtered_keys = [key for key, val in gens.items() if val == value]
        avg_key = tuple(sum(x) / len(filtered_keys) for x in zip(*filtered_keys))
        result[avg_key] = list(value)

    # Sorting the dictionary by values in ascending order
    sorted_result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}

    print("\nBest Combination:", best_selection, best_mutation, best_crossover)

    return sorted_result, best_representation, best_fitness


# Define the function for visualization
def visualization(sorted_result, best_representation):
    # Get the column names from the keys of sorted_result
    column_names = [str(combination) for combination in sorted_result.values()]

    # Get the data for the table (every 100th element from each key)
    data = [[key[i] for key in sorted_result.keys()] for i in range(99, 1001, 100)]

    # Print the table
    print(tabulate(data, headers=column_names, showindex=True, tablefmt="psql"))

    # Create dictionaries for diet quantities and prices
    diet_quantities = {food_names[i]: round(best_representation[i], 4) for i in range(len(food_names))}
    diet_quantities = {k: v for k, v in sorted(diet_quantities.items(), key=lambda item: item[1], reverse=True) if
                       v != 0}

    diet_price = {food_names[i]: round(best_representation[i] * price[i], 4) for i in range(len(price))}
    diet_price = {k: v for k, v in sorted(diet_price.items(), key=lambda item: item[1], reverse=True) if v != 0}

    merged_dict = {}
    for food_name in food_names:
        if food_name in diet_quantities and food_name in diet_price:
            merged_dict[food_name] = (diet_quantities[food_name], diet_price[food_name])

    print("\nBest annual Diet: ")
    print("\nOptimal annual price:", round(best_fitness, 4), "€")
    print("\nAnnual foods:")
    for food_name, (quantity, cost) in merged_dict.items():
        print(f"{food_name} Price: {cost} €, Quantity: {quantity}x;")

    # Calculate nutrient totals and goals
    diet_nutrients = {food_names[i]: [best_representation[i] * nutrient for nutrient in foods[i]] for i in
                      range(len(food_names))}
    nutrient_totals = {nutrient_names[i]: sum(nutrient[i] for nutrient in diet_nutrients.values()) for i in
                       range(len(nutrient_names))}

    nutrient_goals = {nutrient_names[i]: goal[i] for i in range(len(nutrient_names))}

    # Calculate nutrient differences
    nutrient_diff = {key: nutrient_totals[key] - nutrient_goals[key] for key in nutrient_goals}

    print("\nNutrients per year:")
    for nutrient_name, nutrient_value in nutrient_totals.items():
        diff = nutrient_diff[nutrient_name]  # Get the corresponding nutrient difference
        print(f"{nutrient_name}: {nutrient_value} (Diff: {diff})")

    # Plotting the keys from result with updated legend
    for key, value in sorted_result.items():
        generations = np.arange(1, len(key) + 1)
        label = ', '.join(mapping_dict[tuple(value)])
        plt.plot(generations, key, label=label)

    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.legend()
    return plt.show()


# Call the functions to evaluate hyperparameters and visualize the results
sorted_result, best_representation, best_fitness = evaluate_hyperparams(selection, mutation, crossover, 2)
visualization(sorted_result, best_representation)
