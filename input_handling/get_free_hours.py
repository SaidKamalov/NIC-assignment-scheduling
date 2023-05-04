import json
import os


def get_number_of_classes_per_day(study_year: str, track: str, path: str) -> dict[str, int] | None:
    """
    Returns the number of classes per day for each day of the week.
    """
    number_of_classes = json.load(open(path))
    return number_of_classes.get(study_year, {}).get(track, None)


def get_free_hours_per_day(study_year: str, track: str, path: str) -> dict[str, float] | None:
    """
    Returns the number of free hours per day for each day of the week.
    """
    number_of_classes = get_number_of_classes_per_day(study_year, track, path)
    if number_of_classes is None:
        return None
    free_hours = {}
    for day, number in number_of_classes.items():
        if day in ["5", "6"]:
            free_hours[day] = 6 - number * 1.5
        else:
            free_hours[day] = 10 - number * 1.5

    return free_hours
