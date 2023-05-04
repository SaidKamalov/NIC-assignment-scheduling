from assignment import Assignment, get_assignments
from datetime import date, timedelta
from collections import OrderedDict
from copy import deepcopy
from random import randint
from input_handling.get_free_hours import get_free_hours_per_day

AVG_STUDY_HOURS_PER_DAY = 6
PATH = "input_handling/inno_number_of_classes.json"


class Schedule:
    """Just prototype with random initialization"""

    def __init__(
            self,
            path: str | None = None,
            study_year: str | None = None,
            track: str | None = None,
            num_of_assignments: int = 5,
    ) -> None:
        self.assignments: list[Assignment] = get_assignments(
            path=path, num_of_assignments=num_of_assignments
        )
        # The earliest and the latest date for all assignments
        self.start: date
        self.end: date
        self.days: OrderedDict[date, float] = OrderedDict()

        self.study_year: str = study_year
        self.track: str = track

        self._add_assignments()

    def _add_assignments(self) -> None:
        self.assignments = sorted(self.assignments)
        first_date = self.assignments[0].start_date
        last_date = self.assignments[-1].end_date

        self.start = deepcopy(first_date)
        self.end = deepcopy(last_date)

        if self.study_year is not None and self.track is not None:
            free_hours = get_free_hours_per_day(self.study_year, self.track, PATH)
            if len(free_hours) == 0:
                raise ValueError(
                    "No free hours found for the given study year and track"
                )
        else:
            free_hours = {str(i): randint(0, AVG_STUDY_HOURS_PER_DAY) for i in range(7)}

        for day in range((last_date - first_date).days + 1):
            new_date = first_date + timedelta(days=day)
            self.days[new_date] = float(free_hours[str(new_date.weekday())])

    def get_free_time(self, from_: date, to: date, include_weekends: bool = False):
        delta = abs((to - from_).days)
        free_hours = 0.0
        for day in range(0, delta + 1):
            new_date = from_ + timedelta(days=day)
            if not include_weekends and new_date.weekday() in [5, 6]:
                continue
            free_hours += self.days.get(from_ + timedelta(days=day), 0)
        return free_hours
