import random

from genetic_algorithm import GeneticAlgorithm, Chromosome


def test_genetic_algorithm():
    print('-' * 20)
    print("Running tests for genetic_algorithm.py")

    print("1) Testing Chromosome class")
    chromosome = Chromosome([1, 2, 3, 4, 5])
    assert chromosome.genes == [1, 2, 3, 4, 5]

    print("2) Testing GeneticAlgorithm class")
    ga = GeneticAlgorithm(
        possible_genes=[1, 2, 3, 4, 5],
        population_size=10,
        fitness_func=None,
        crossover_func=None,
        mutate_func=None,
        mutation_rate=0.1,
        elite_size=2,
        early_stop=5
    )
    assert ga.early_stop == 5
    ga.run(3)
    assert len(ga.population) == 10
    assert len(ga.elite) == 2

    print("3) Testing GeneticAlgorithm class with fitness_func")

    def fitness_func(genes):
        return sum(genes)

    ga = GeneticAlgorithm(
        possible_genes=[1, 2, 3, 4, 5],
        population_size=10,
        fitness_func=fitness_func,
        crossover_func=None,
        mutate_func=None,
        mutation_rate=0.1,
        elite_size=2,
        early_stop=5
    )
    assert ga.early_stop == 5
    ga.run(3)
    assert len(ga.population) == 10
    assert len(ga.elite) == 2

    print("4) Testing GeneticAlgorithm class with crossover_func")

    def crossover_func(parent1, parent2):
        child1 = parent1[: len(parent1) // 2] + parent2[len(parent2) // 2:]
        child2 = parent2[: len(parent2) // 2] + parent1[len(parent1) // 2:]
        return child1, child2

    ga = GeneticAlgorithm(
        possible_genes=[1, 2, 3, 4, 5],
        population_size=10,
        fitness_func=None,
        crossover_func=crossover_func,
        mutate_func=None,
        crossover_rate=1,
        elite_size=2,
        early_stop=5
    )
    assert ga.early_stop == 5
    ga.run(3)
    assert len(ga.population) == 10
    assert len(ga.elite) == 2

    print("5) Testing GeneticAlgorithm class with mutate_func")

    def mutate_func(genes, mutation_rate):
        for i in range(len(genes)):
            if random.random() < mutation_rate:
                genes[i] = random.choice([1, 2, 3, 4, 5])
        return genes

    ga = GeneticAlgorithm(
        possible_genes=[1, 2, 3, 4, 5],
        population_size=10,
        fitness_func=None,
        crossover_func=None,
        mutate_func=mutate_func,
        mutation_rate=1,
        elite_size=2,
        early_stop=5
    )
    assert ga.early_stop == 5
    ga.run(3)
    assert len(ga.population) == 10
    assert len(ga.elite) == 2


if __name__ == '__main__':
    test_genetic_algorithm()
