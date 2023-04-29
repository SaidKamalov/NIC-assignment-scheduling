from assignment import Assignment, get_assignments
from datetime import date, timedelta
from collections import OrderedDict
from copy import deepcopy
from random import randint


HOURS_PER_DAY = 6  # zaglushka


class Schedule:
    """Just prototype with random initialization"""

    # TODO: add import of a real schedule
    def __init__(self, path: str | None = None) -> None:
        self.assignments: list[Assignment] = get_assignments(
            path=path, num_of_assignments=3
        )
        # The earliest and the latest date for all assignments
        self.start: date
        self.end: date
        self.days: OrderedDict[date, float] = OrderedDict()
        self._add_assignments()

    def _add_assignments(self, path: str | None = None) -> None:
        self.assignments = sorted(self.assignments)
        first_date = self.assignments[0].start_date
        last_date = self.assignments[-1].end_date

        self.start = deepcopy(first_date)
        self.end = deepcopy(last_date)

        print(f"from: {self.start} to {self.end}")

        for day in range((last_date - first_date).days + 1):
            self.days[first_date + timedelta(days=day)] = randint(0, HOURS_PER_DAY)


if __name__ == "__main__":
    # TODO: remove, just for testing
    test_schedule = Schedule()
    for k, v in test_schedule.days.items():
        print(k, v)
