from datetime import date
from input_handling.input import _read_assignments, _generate_assignments


# TODO: to be tested
class Assignment:
    def __init__(
        self,
        name: str,
        start_date: date,
        end_date: date,
        hours_to_complete: int,
        include_weekends: bool,
    ) -> None:
        self.name = name
        self.hours_to_complete = hours_to_complete
        self.include_weekends = include_weekends
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self) -> str:
        res = (
            f"{self.name}: need {self.hours_to_complete} hours to complete\n"
            + f"can be from {self.start_date.year}-{self.start_date.month}-{self.start_date.day} "
            + f"to {self.end_date.year}-{self.end_date.month}-{self.end_date.day}"
        )
        return res


def get_assignments(
    path: str | None = None, num_of_assignments: int = 10, **kwargs
) -> list[Assignment]:
    if path == None:
        assignments = [
            Assignment(**assignment)
            for assignment in _generate_assignments(10, **kwargs)
        ]
    else:
        assignments = [
            Assignment(**assignment) for assignment in _read_assignments(path)
        ]
    return assignments


if __name__ == "__main__":
    # TODO: remove, just for testing
    for ass in get_assignments("./input_handling/assignments-example.json"):
        print(ass)
    print("generated:")
    for ass in get_assignments(
        num_of_assignments=5, max_day_range=10, include_weekends_prob=0.9
    ):
        print(ass)
