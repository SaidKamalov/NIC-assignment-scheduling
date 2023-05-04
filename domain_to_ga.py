from assignment import Assignment
from datetime import date, timedelta
from random import randint, random
from copy import deepcopy
from schedule import Schedule

PATH = "input_handling/inno_assignments.json"
TRACK = "DS"
STUDY_YEAR = "BS2"

SCHEDULE = Schedule(
    path=PATH, study_year=STUDY_YEAR, track=TRACK, num_of_assignments=20
)


class AssignmentGene:
    def __init__(self, assignment: Assignment) -> None:
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
        Function to get the time slot for the assignment in the give gene.
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
    """Function to create new chromosome"""
    genes_for_chromo: list[AssignmentGene] = [
        generate_rand_gene(gene) for gene in genes
    ]
    return genes_for_chromo


def generate_rand_gene(gene: AssignmentGene) -> AssignmentGene:
    """
    Function to create copy of a given gene,
    but assign random time slot for the assignment.
    """
    new_gene = AssignmentGene(gene.assignment)
    new_gene.start, new_gene.deadline = new_gene.rand_time_slot()
    return new_gene


def random_mutate_genes(
    genes: list[AssignmentGene], mutation_rate: float, *args
) -> None:
    for gene in genes:
        if random() < mutation_rate:
            gene.start, gene.deadline = gene.rand_time_slot()


def fitness(genes: list[AssignmentGene]):
    genes_sorted = sorted(genes)

    # count overlapping
    overlap_count = 0
    for i in range(len(genes_sorted) - 1):
        if genes_sorted[i].deadline > genes_sorted[i + 1].start:
            overlap_count += 1

    # check time
    time_issues = 0
    for gene in genes:
        available_time = SCHEDULE.get_free_time(
            from_=gene.start,
            to=gene.deadline,
            include_weekends=gene.assignment.include_weekends,
        )
        if available_time < gene.assignment.hours_to_complete:
            time_issues += 1

        if (
            gene.assignment.hours_to_complete
            > (gene.deadline - gene.start).days * 24 * 0.1
        ):
            time_issues += 1
        if gene.assignment.hours_to_complete < 0.3 * available_time:
            time_issues += 1

    return -(overlap_count + time_issues)


def crossover(
    p1: list[AssignmentGene], p2: list[AssignmentGene]
) -> tuple[list[AssignmentGene], list[AssignmentGene]]:
    # p1, p2 = sorted(parent1), sorted(parent2)
    c1: list[AssignmentGene] = [AssignmentGene(gene.assignment) for gene in p1]
    c2: list[AssignmentGene] = [AssignmentGene(gene.assignment) for gene in p2]
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


if __name__ == "__main__":
    # TODO: remove, just for testing
    print("Assignment list:")
    for assignment in SCHEDULE.assignments:
        print(assignment)
    print()
    print("list possible genes:")
    possible_genes = [AssignmentGene(assignment) for assignment in SCHEDULE.assignments]
    for gene in possible_genes:
        print(gene)
    print()
    print("list genes in chromosome")
    genes_for_chromo = generate_chromo(possible_genes)
    for gene in genes_for_chromo:
        print(gene)
    print()
    print("list chromosome genes after mutation")
    random_mutate_genes(genes_for_chromo, mutation_rate=0.8)
    for gen in genes_for_chromo:
        print(gen)
    print()
    fitness_score = fitness(genes=genes_for_chromo)
    print("fitness sore of chromo", fitness_score)
    print("##########")
    print("test custom crossover:")
    parent1 = generate_chromo(possible_genes)
    print("parent1:")
    for gene in parent1:
        print(gene)
    print()
    parent2 = generate_chromo(possible_genes)
    print("parent2:")
    for gene in parent2:
        print(gene)
    print()
    c1, c2 = crossover(parent1, parent2)
    print("child1:")
    for gene in c1:
        print(gene)
    print()
    print("child2:")
    for gene in c2:
        print(gene)
    print()
