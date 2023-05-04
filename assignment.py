from datetime import date
from input_handling.input import _read_assignments, _generate_assignments


class Assignment:
    def __init__(
        self,
        name: str,
        start_date: date,
        end_date: date,
        hours_to_complete: int,
        include_weekends: bool,
    ):
        self.name: str = name
        self.hours_to_complete: int = hours_to_complete
        self.include_weekends: bool = include_weekends
        self.start_date: date = start_date
        self.end_date: date = end_date

    def __str__(self) -> str:
        res = (
            f"{self.name}: need {self.hours_to_complete} hours to complete\n"
            + f"can be from {self.start_date} to {self.end_date}."
        )
        return res

    def __lt__(self, other) -> bool:
        if self.start_date == other.start_date:
            return self.end_date < other.end_date
        else:
            return self.start_date < other.start_date


def get_assignments(path: str | None = None, **kwargs) -> list[Assignment]:
    if path is None:
        assignments = [
            Assignment(**assignment) for assignment in _generate_assignments(**kwargs)
        ]
    else:
        assignments = [
            Assignment(**assignment) for assignment in _read_assignments(path)
        ]
    return assignments


if __name__ == "__main__":
    pass
