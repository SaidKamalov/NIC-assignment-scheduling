from assignment import Assignment
from datetime import date, timedelta
from random import randint, choice, random
from copy import deepcopy
from genetic_algorithm import Chromosome
from schedule import Schedule

PATH_TO_SCHEDULE = ""


class AssignmentGene:
    def __init__(self, assignment: Assignment) -> None:
        self.assignment = assignment
        self.start: date = deepcopy(self.assignment.start_date)
        self.deadline: date = deepcopy(self.assignment.end_date)
        self.score: float = 0

    def __str__(self) -> str:
        res = str(self.assignment) + "\n"
        res += f"suggested slot: from {self.start} to {self.deadline}.\n"
        res += f"It is {(self.deadline - self.start).days} days for {self.assignment.hours_to_complete} hours of work.\n"
        res += f"score is {self.score}"
        return res

    def rand_time_slot(self) -> tuple[date, date]:
        """
        Function to get the time slot for the assignment in the give gene.
        Time slot is in [assignment.start_date; assignment.end_date].
        """
        end_date = self.assignment.end_date
        start_date = self.assignment.start_date
        delta = end_date - start_date
        duration = randint(2, delta.days)
        free_time = delta.days - duration

        start = start_date + timedelta(days=randint(0, free_time))
        deadline = start + timedelta(days=duration)
        return start, deadline


def generate_chromo(genes: list[AssignmentGene]) -> Chromosome:
    """Function to create new chromosome"""
    genes_for_chromo = [generate_rand_gene(gene) for gene in genes]
    chromo = Chromosome(genes_for_chromo)
    return chromo


def generate_rand_gene(genes: list[AssignmentGene]) -> AssignmentGene:
    """
    Function to create copy of a given gene,
    but assign random time slot for the assignment.
    """
    new_gene = AssignmentGene(choice(genes).assignment)
    new_gene.start, new_gene.deadline = new_gene.rand_time_slot()
    return new_gene


def random_mutate_time_slot(
    population: list[Chromosome], mutation_rate: float, *args
) -> list[Chromosome]:
    """
    Function to mutate population.
    """
    for i in range(len(population)):
        for j in range(len(population[i].genes)):
            if random() < mutation_rate:
                population[i].genes[j].start_date, population[i].genes[j].end_date = (
                    population[i].genes[j].rand_time_slot()
                )
    return population


class Fitness:
    _SCHEDULE = Schedule(PATH_TO_SCHEDULE)

    @staticmethod
    def fitness(genes: list[AssignmentGene]):
        assignments = sorted([gene.assignment for gene in genes])
        pass


if __name__ == "__main__":
    # TODO: remove, just for testing
    from input_handling.input import _generate_assignments

    assignments = [Assignment(**ass) for ass in _generate_assignments(2)]
    genes = [AssignmentGene(ass) for ass in assignments]
    print("initial genes:")
    for gene in genes:
        print(gene)
    print()
    print("generated chromo:")
    chromo = generate_chromo(genes)
    for gene in chromo.genes:
        print(gene)
    print()
    print("check initial genes:")
    for gene in genes:
        print(gene)
