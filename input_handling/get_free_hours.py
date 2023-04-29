import json


def get_number_of_classes_per_day(study_year: str, track: str) -> dict[str, int] | None:
    """
    Returns the number of classes per day for each day of the week.
    """
    number_of_classes = json.load(open('input_handling/inno_number_of_classes.json'))
    return number_of_classes.get(study_year, {}).get(track, None)


def get_free_hours_per_day(study_year: str, track: str) -> dict[str, float] | None:
    """
    Returns the number of free hours per day for each day of the week.
    """
    number_of_classes = get_number_of_classes_per_day(study_year, track)
    if number_of_classes is None:
        return None
    free_hours = {}
    for day, number in number_of_classes.items():
        # TODO: determine the suitable number of studying hours on weekends
        if day in ['5', '6']:
            free_hours[day] = 6 - number * 1.5
        else:
            free_hours[day] = 10 - number * 1.5

    return free_hours


if __name__ == '__main__':
    # TODO: remove, just for testing
    print(get_free_hours_per_day('BS1', 'CS'))
