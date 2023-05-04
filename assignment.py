from datetime import date
from input_handling.input import _read_assignments, _generate_assignments


class Assignment:
    """
    A class to represent an assignment.
    """

    def __init__(
            self,
            name: str,
            start_date: date,
            end_date: date,
            hours_to_complete: int,
            include_weekends: bool,
    ):
        """
        :param name: Name of the assignment
        :param start_date: The date the assignment can start
        :param end_date: The date the assignment must be completed by
        :param hours_to_complete: The number of hours the assignment will take to complete
        :param include_weekends: Whether or not the assignment can be completed on weekends
        """
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
    """
    Gets a list of assignments from a file or generates them from kwargs
    :param path: the path to the file containing the assignments
    :param kwargs: the kwargs to generate the assignments from
    :return: a list of assignments
    """
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
