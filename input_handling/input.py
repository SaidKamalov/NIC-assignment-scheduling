import json
import datetime
from datetime import date, timedelta
from random import randint, random
import environment

ASSIGNMENT_FIELDS = {
    "name",
    "start_date",
    "end_date",
    "hours_to_complete",
    "include_weekends",
}


def check_structure(assignment: dict) -> bool:
    if set(assignment.keys()) != ASSIGNMENT_FIELDS:
        print("Error while reading assignments from json file: " "invalid fields")
        return False

    elif (
        not isinstance(assignment["name"], str)
        or not isinstance(assignment["start_date"], str)
        or not isinstance(assignment["end_date"], str)
        or not isinstance(assignment["hours_to_complete"], int)
        or not isinstance(assignment["include_weekends"], bool)
    ):
        print("Error while reading assignments from json file: " "invalid field types")
        return False

    elif assignment["start_date"] > assignment["end_date"]:
        print(
            "Error while reading assignments from json file: "
            "start_date is greater than end_date"
        )
        return False

    elif assignment["hours_to_complete"] <= 0:
        print(
            "Error while reading assignments from json file: "
            "hours_to_complete is less than or equal to zero"
        )
        return False

    else:
        try:
            # convert start_date to date obj
            start_date = list(map(int, assignment["start_date"].split("-")))
            # convert end_date to date obj
            end_date = list(map(int, assignment["end_date"].split("-")))
            return True
        except Exception as e:
            print("Error while reading assignments from json file:", e)
            return False


def _read_assignments(path_to_json: str):
    with open(path_to_json, "r") as file:
        assignments = json.load(file)
        for assignment in assignments["assignments"]:
            if "include_weekends" not in assignment:
                assignment["include_weekends"] = False
            if not check_structure(assignment):
                yield None
            else:
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
    if (
        num_of_assignments <= 0
        or max_day_range <= 0
        or min_day_range <= 0
        or working_hours_ratio <= 0
        or working_hours_ratio > 1
        or include_weekends_prob <= 0
        or include_weekends_prob > 1
        or max_day_range < min_day_range
    ):
        print("Error while generating assignments: invalid arguments")
        return

    year: int = 2023 + randint(-2, 0)
    for i in range(num_of_assignments):
        assignment = {
            "name": f"Assignment {i}",
            "include_weekends": (False if random() > include_weekends_prob else True),
        }
        start = datetime.date(year, 1, 1)
        end = datetime.date(year, 12, 31)
        delta = end - start
        rand_delta = randint(0, delta.days - max_day_range)
        start_date = start + timedelta(days=rand_delta)
        end_date = start_date + timedelta(days=randint(min_day_range, max_day_range))
        assignment["start_date"] = start_date
        assignment["end_date"] = end_date

        hours = int((end_date - start_date).days * 24 * working_hours_ratio)
        if hours <= 0:
            hours = 2
        assignment["hours_to_complete"] = randint(2, hours)

        yield assignment


def get_number_of_classes_per_day(
    study_year: str, track: str, path
) -> dict[str, int] | None:
    """
    Returns the number of classes per day for each day of the week.
    """
    number_of_classes = json.load(open(path))
    return number_of_classes.get(study_year, {}).get(track, None)


def get_free_hours_per_day(
    study_year: str, track: str, path
) -> dict[str, float] | None:
    """
    Returns the number of free hours per day for each day of the week.
    """
    number_of_classes = get_number_of_classes_per_day(study_year, track, path)
    if number_of_classes is None:
        return None
    free_hours = {}
    for day, number in number_of_classes.items():
        # TODO: determine the suitable number of studying hours on weekends
        if day in ["5", "6"]:
            free_hours[day] = 6 - number * 1.5
        else:
            free_hours[day] = 10 - number * 1.5

    return free_hours


if __name__ == "__main__":
    for assignment in _read_assignments("../tests/test-assignments.json"):
        print(assignment)
