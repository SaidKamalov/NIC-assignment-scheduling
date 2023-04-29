from assignment import Assignment
from datetime import date, timedelta
from random import randint
from copy import deepcopy
from genetic_algorithm import Chromosome


class Gen:
    def __init__(self, assignment: Assignment) -> None:
        self.assignment = assignment
        self.start: date = deepcopy(self.assignment.start_date)
        self.deadline: date = deepcopy(self.assignment.end_date)
        self.score: float = 0

    def __str__(self) -> str:
        res = str(self.assignment) + "\n"
        res += f"suggested slot: from {self.start} to {self.deadline}.\n"
        res += f"It is {(self.deadline-self.start).days} days for {self.assignment.hours_to_complete} hours of work.\n"
        res += f"score is {self.score}"
        return res

    def rand_time_slot(self) -> tuple[date, date]:
        end_date = self.assignment.end_date
        start_date = self.assignment.start_date
        delta = end_date - start_date
        duration = randint(2, delta.days)
        free_time = delta.days - duration

        start = start_date + timedelta(days=randint(0, free_time))
        deadline = start + timedelta(days=duration)
        return start, deadline


def generate_chromo(genes: list[Gen]) -> Chromosome:
    genes_for_chromo = [generate_rand_gen(gen) for gen in genes]
    chromo = Chromosome(genes_for_chromo)
    return chromo


def generate_rand_gen(gen: Gen) -> Gen:
    new_gen = Gen(gen.assignment)
    new_gen.start, new_gen.deadline = gen.rand_time_slot()
    return new_gen


if __name__ == "__main__":
    # TODO: remove, just for testing
    from input_handling.input import _generate_assignments

    assignments = [Assignment(**ass) for ass in _generate_assignments(2)]
    genes = [Gen(ass) for ass in assignments]
    print("initial genes:")
    for gen in genes:
        print(gen)
    print()
    print("generated chromo:")
    chromo = generate_chromo(genes)
    for gen in chromo.genes:
        print(gen)
    print()
    print("check initial genes:")
    for gen in genes:
        print(gen)
