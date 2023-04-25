import random


class Chromosome:
    def __init__(self, genes: list) -> None:
        self.genes: list = genes
        self.fitness: int = 0

    def __str__(self) -> str:
        return str(self.genes)

    def __repr__(self) -> str:
        return str(self.genes)


class GeneticAlgorithm:
    def __init__(self, possible_genes: list,
                 population_size: int = 500, elite_size: int = 200,
                 mutation_rate: float = 0.2,
                 crossover_rate: float = 0.5,
                 mutate_func=None,
                 crossover_func=None,
                 generate_func=None,
                 fitness_func=None) -> None:
        self.possible_genes: list = possible_genes
        self.population_size: int = population_size
        self.elite_size: int = elite_size
        self.mutation_rate: float = mutation_rate
        self.crossover_rate: float = crossover_rate
        self.mutate_func = mutate_func
        self.crossover_func = crossover_func
        self.generate_func = generate_func
        self.fitness_func = fitness_func

        self.population: list[Chromosome] = []
        self.elite: list[Chromosome] = []

    def _generate_chromosome(self) -> Chromosome:
        if self.generate_func:
            return self.generate_func(self.possible_genes)

        return Chromosome(random.choices(self.possible_genes, k=len(self.possible_genes)))

    def _get_elite(self) -> list[Chromosome]:
        return sorted(self.population, key=lambda x: x.fitness, reverse=True)[:self.elite_size]

    def crossover(self) -> None:
        if self.crossover_func:
            self.population = self.crossover_func(self.population, self.crossover_rate)

        for i in range(self.elite_size, self.population_size):
            if random.random() < self.crossover_rate:
                parent1 = random.choice(self.elite)
                parent2 = random.choice(self.elite)
                child = parent1.genes[:len(parent1.genes) // 2] + parent2.genes[len(parent2.genes) // 2:]
                self.population[i] = Chromosome(child)

    def mutate(self) -> None:
        if self.mutate_func:
            self.population = self.mutate_func(self.population, self.mutation_rate, self.possible_genes)

        for i in range(self.elite_size, self.population_size):
            for j in range(len(self.population[i].genes)):
                if random.random() < self.mutation_rate:
                    self.population[i].genes[j] = random.choice(self.possible_genes)

    def initialize(self) -> None:
        self.population = [self._generate_chromosome() for _ in range(self.population_size)]
        self.elite = self._get_elite()

    def calculate_fitness(self) -> None:
        for chromosome in self.population:
            chromosome.fitness = (self.fitness_func(chromosome) if self.fitness_func else sum(chromosome.genes))
            self.elite = self._get_elite()

    def evolve(self) -> None:
        self.crossover()
        self.mutate()
        self.calculate_fitness()

    def get_best(self) -> Chromosome:
        return self.elite[0]

    def run(self, num_of_generations: int) -> Chromosome:
        self.initialize()
        for _ in range(num_of_generations):
            self.evolve()
        return self.get_best()


if __name__ == "__main__":
    # TODO: remove, just for testing
    print(GeneticAlgorithm(possible_genes=[1, 2, 3, 4, 5]).run(10))
