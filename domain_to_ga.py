"""
ALl the functions and classes that are needed to convert the domain to the GA.
"""
from assignment import Assignment
from datetime import date, timedelta
from random import randint, random
from copy import deepcopy
from schedule import Schedule
import environment

PATH = environment.PATH_TO_ASSIGNMENTS
TRACK = environment.TRACK
STUDY_YEAR = environment.STUDY_YEAR

SCHEDULE = Schedule(
    path=PATH,
    study_year=STUDY_YEAR,
    track=TRACK,
    num_of_assignments=environment.NUMBER_OF_ASSIGNMENTS,
)


class AssignmentGene:
    """
    Class to represent the gene for the assignment.
    Gene is a time slot for the assignment.
    """

    def __init__(self, assignment: Assignment) -> None:
        """
        :param assignment: assignment for the gene
        """
        self.assignment: Assignment = assignment
        self.start: date = deepcopy(self.assignment.start_date)
        self.deadline: date = deepcopy(self.assignment.end_date)

    def __str__(self) -> str:
        res = str(self.assignment) + "\n"
        res += f"suggested slot: from {self.start} to {self.deadline}.\n"
        res += f"It is {(self.deadline - self.start).days} days for {self.assignment.hours_to_complete} hours of work.\n"
        return res

    def __lt__(self, other) -> bool:
        if self.start == other.start:
            return self.deadline <= other.deadline
        else:
            return self.start < other.start

    def rand_time_slot(self) -> tuple[date, date]:
        """
        Gets the time slot for the assignment in the give gene.
        Time slot is in [assignment.start_date; assignment.end_date].
        """
        end_date: date = self.assignment.end_date
        start_date: date = self.assignment.start_date
        delta: timedelta = end_date - start_date
        duration: int = randint(2, delta.days)
        free_time: int = delta.days - duration

        start: date = start_date + timedelta(days=randint(0, free_time))
        deadline: date = start + timedelta(days=duration)
        return start, deadline


def generate_chromo(genes: list[AssignmentGene]) -> list[AssignmentGene]:
    """
    Generates a chromosome for the given genes.
    :param genes: list of genes
    :return: generated genes for the chromosome
    """
    genes_for_chromo: list[AssignmentGene] = [
        generate_rand_gene(gene) for gene in genes
    ]
    return genes_for_chromo


def generate_rand_gene(gene: AssignmentGene) -> AssignmentGene:
    """
    Creates copy of a given gene,
    but assigns random time slot for the assignment.
    """
    new_gene = AssignmentGene(gene.assignment)
    new_gene.start, new_gene.deadline = new_gene.rand_time_slot()
    return new_gene


def random_mutate_genes(
        genes: list[AssignmentGene], mutation_rate: float
) -> None:
    """
    Mutates the given genes with the given mutation rate.
    :param genes: list of genes to mutate
    :param mutation_rate: mutation rate
    :return: None
    """
    for gene in genes:
        if random() < mutation_rate:
            gene.start, gene.deadline = gene.rand_time_slot()


def fitness(genes: list[AssignmentGene]) -> float:
    """
    Calculates the fitness of the given genes.
    :param genes: genes to calculate fitness for
    :return: fitness of the given genes
    """
    genes_sorted = sorted(genes)

    # count overlapping
    overlap_count = 0
    for i in range(len(genes_sorted) - 1):
        if genes_sorted[i].deadline > genes_sorted[i + 1].start:
            overlap_count += 1.5

    # check time
    time_issues = 0
    for gene in genes:
        available_time = SCHEDULE.get_free_time(
            from_=gene.start,
            to=gene.deadline,
            include_weekends=gene.assignment.include_weekends,
        )
        if available_time < gene.assignment.hours_to_complete:
            time_issues += 0.5

        if (
                gene.assignment.hours_to_complete
                > (gene.deadline - gene.start).days * 24 * 0.1
        ):
            time_issues += 2
        if gene.assignment.hours_to_complete < 0.3 * available_time:
            time_issues += 2

    return -(overlap_count + time_issues)


def crossover(
        p1: list[AssignmentGene], p2: list[AssignmentGene]
) -> tuple[list[AssignmentGene], list[AssignmentGene]]:
    """
    Crossover for the given parents.
    :param p1: parent 1
    :param p2: parent 2
    :return: children
    """
    c1: list[AssignmentGene] = [AssignmentGene(gene.assignment) for gene in p1]
    c2: list[AssignmentGene] = [AssignmentGene(gene.assignment) for gene in p2]
    for i, gene1 in enumerate(c1):
        gene1.start, gene1.deadline = deepcopy(p1[i].start), deepcopy(p1[i].deadline)
    for i, gene2 in enumerate(c2):
        gene2.start, gene2.deadline = deepcopy(p2[i].start), deepcopy(p2[i].deadline)

    for i in range(len(p1) - 1):
        if p1[i].deadline > p1[i + 1].start >= p2[i].deadline:
            c1[i].start, c1[i].deadline = deepcopy(p2[i].start), deepcopy(
                p2[i].deadline
            )
        elif p2[i].deadline > p2[i + 1].start >= p1[i].deadline:
            c2[i].start, c2[i].deadline = deepcopy(p1[i].start), deepcopy(
                p1[i].deadline
            )
    return c1, c2


def crossover_v2(
        p1: list[AssignmentGene], p2: list[AssignmentGene]
) -> tuple[list[AssignmentGene], list[AssignmentGene]]:
    """
    Crossover for the given parents.(Modification of the crossover() function)
    :param p1: parent 1
    :param p2: parent 2
    :return: children
    """
    c1: list[AssignmentGene] = [AssignmentGene(gene.assignment) for gene in p1]
    c2: list[AssignmentGene] = [AssignmentGene(gene.assignment) for gene in p2]
    for i, gene1 in enumerate(c1):
        gene1.start, gene1.deadline = deepcopy(p1[i].start), deepcopy(p1[i].deadline)
    for i, gene2 in enumerate(c2):
        gene2.start, gene2.deadline = deepcopy(p2[i].start), deepcopy(p2[i].deadline)
    c1_new = c1[: len(c1) // 2] + c2[len(c2) // 2:]
    c2_new = c2[: len(c2) // 2] + c1[len(c1) // 2:]
    return c1_new, c2_new


if __name__ == "__main__":
    pass
