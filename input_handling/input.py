import json
import datetime
from datetime import date, timedelta
from random import randint, random


def _read_assignments(path_to_json: str):
    with open(path_to_json, "r") as file:
        assignments = json.load(file)
        for assignment in assignments["assignments"]:
            # convert start_date to date obj
            start_date = list(map(int, assignment["start_date"].split("-")))
            assignment["start_date"] = date(
                year=start_date[0], month=start_date[1], day=start_date[2]
            )
            # convert end_date to date obj
            end_date = list(map(int, assignment["end_date"].split("-")))
            assignment["end_date"] = date(
                year=end_date[0], month=end_date[1], day=end_date[2]
            )
            yield assignment


def _generate_assignments(
    num_of_assignments: int,
    max_day_range: int = 30,
    min_day_range: int = 2,
    working_hours_ratio: float = 0.1,
    include_weekends_prob: float = 0.3,
):
    year = 2023 + randint(-2, 0)
    for i in range(num_of_assignments):
        assignment = {}
        assignment["name"] = f"Assignment {i}"
        assignment["include_weekends"] = (
            False if random() > include_weekends_prob else True
        )
        start = datetime.date(year, 1, 1)
        end = datetime.date(year, 12, 31)
        delta = end - start
        rand_delta = randint(0, delta.days - max_day_range)
        start_date = start + timedelta(days=rand_delta)
        end_date = start_date + timedelta(days=randint(min_day_range, max_day_range))
        assignment["start_date"] = start_date
        assignment["end_date"] = end_date

        assignment["hours_to_complete"] = randint(
            2, int((end_date - start_date).days * 24 * working_hours_ratio)
        )

        yield assignment


if __name__ == "__main__":
    pass
