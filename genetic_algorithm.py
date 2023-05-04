import random
from copy import deepcopy
import environment
import tqdm


class Chromosome:
    def __init__(self, genes: list) -> None:
        self.genes: list = genes
        self.fitness: int = 0

    def __str__(self) -> str:
        return "\n".join(map(str, self.genes)) + f"\nchromosome score = {self.fitness}"

    def __repr__(self) -> str:
        return str(self.genes)


class GeneticAlgorithm:
    def __init__(
        self,
        possible_genes: list,
        population_size: int = 500,
        elite_size: int = 200,
        mutation_rate: float = 0.2,
        crossover_rate: float = 0.5,
        early_stop: int = 3,
        mutate_func=None,
        crossover_func=None,
        generate_func=None,
        fitness_func=None,
    ) -> None:
        self.possible_genes: list = possible_genes
        self.population_size: int = population_size
        self.elite_size: int = elite_size
        self.mutation_rate: float = mutation_rate
        self.crossover_rate: float = crossover_rate
        self.early_stop: int = early_stop
        self.mutate_func = mutate_func
        self.crossover_func = crossover_func
        self.generate_func = generate_func
        self.fitness_func = fitness_func

        self.population: list[Chromosome] = []
        self.elite: list[Chromosome] = []

    def _generate_chromosome(self) -> Chromosome:
        if self.generate_func:
            new_chromosome = Chromosome(self.generate_func(self.possible_genes))
            return new_chromosome

        return Chromosome(
            random.choices(self.possible_genes, k=len(self.possible_genes))
        )

    def _get_elite(self) -> list[Chromosome]:
        return sorted(self.population, key=lambda x: x.fitness, reverse=True)[
            : self.elite_size
        ]

    def crossover(self) -> None:
        if self.crossover_func:
            elite = self._get_elite()
            children = []
            for i in range(len(elite)):
                for j in range(i + 1, len(elite)):
                    c1, c2 = self.crossover_func(elite[i].genes, elite[j].genes)
                    children.append(Chromosome(c1))
                    children.append(Chromosome(c2))
            new_pop = elite + children
            self.population = new_pop[: self.population_size]
        else:
            elite = self._get_elite()
            children = []
            for i in range(len(elite)):
                for j in range(i + 1, len(elite)):
                    c1_genes = (
                        elite[i].genes[: len(elite[i].genes) // 2]
                        + elite[j].genes[len(elite[j].genes) // 2 :]
                    )
                    c2_genes = (
                        elite[j].genes[: len(elite[j].genes) // 2]
                        + elite[i].genes[len(elite[i].genes) // 2 :]
                    )
                    children.append(Chromosome(c1_genes))
                    children.append(Chromosome(c2_genes))
            self.population = (children + elite)[: self.population_size]

    def mutate(self) -> None:
        if self.mutate_func:
            for chromosome in self.population[self.elite_size :]:
                self.mutate_func(chromosome.genes, self.mutation_rate)
        else:
            for i in range(self.elite_size, self.population_size):
                for j in range(len(self.population[i].genes)):
                    if random.random() < self.mutation_rate:
                        self.population[i].genes[j] = deepcopy(
                            random.choice(self.possible_genes)
                        )

    def initialize(self) -> None:
        self.population = [
            self._generate_chromosome() for _ in range(self.population_size)
        ]
        self.elite = self._get_elite()

    def calculate_fitness(self) -> None:
        for chromosome in self.population:
            chromosome.fitness = (
                self.fitness_func(chromosome.genes)
                if self.fitness_func
                else sum(chromosome.genes)
            )
        self.elite = self._get_elite()

    def evolve(self) -> None:
        self.crossover()
        self.mutate()
        self.calculate_fitness()

    def get_best(self) -> Chromosome:
        return self.elite[0]

    def run(self, num_of_generations: int) -> Chromosome:
        print("Starting genetic algorithm...")
        self.initialize()
        best_score = self.get_best().fitness
        init_early_stop = self.early_stop
        bar = tqdm.tqdm(range(num_of_generations))
        for i in bar:
            self.evolve()
            if best_score >= self.get_best().fitness:
                self.early_stop -= 1
            else:
                self.early_stop = init_early_stop
            best_score = self.get_best().fitness

            bar.set_postfix_str(f"Best score: {best_score}")
            if self.early_stop <= 0:
                break

        best_solution = self.get_best()
        print(f"Best solution:\n{best_solution}")

        return best_solution


if __name__ == "__main__":
    from assignment import get_assignments
    from experiments import visualize
    from domain_to_ga import (
        generate_chromo,
        AssignmentGene,
        SCHEDULE,
        fitness,
        random_mutate_genes,
        crossover,
        crossover_v2,
    )

    ga = GeneticAlgorithm(
        possible_genes=[
            AssignmentGene(assignment) for assignment in SCHEDULE.assignments
        ],
        early_stop=environment.EARLY_STOP,
        generate_func=generate_chromo,
        fitness_func=fitness,
        mutate_func=random_mutate_genes,
        crossover_func=crossover,
        mutation_rate=environment.MUTATION_RATE,
        population_size=environment.POPULATION_SIZE,
        elite_size=environment.ELITE_SIZE,
    )
    solution = ga.run(environment.NUM_OF_RUNS)
    visualize(solution.genes)
