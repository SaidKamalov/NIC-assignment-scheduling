from input_handling.get_free_hours import get_free_hours_per_day, get_number_of_classes_per_day
from input_handling.input import _read_assignments, _generate_assignments
from datetime import date
import json


def test_get_free_hours():
    print("Running tests for input_handling/get_free_hours.py")

    variants = {'BS1': ['CS', 'DSAI'],
                'BS2': ['SD', 'CS', 'AI', 'DS', 'RO'],
                'BS3': ['SD', 'CS', 'AI', 'DS', 'RO'],
                'BS4': ['SD', 'CS', 'AI', 'DS', 'RO'],
                'MS1': ['SE', 'DS', 'RO', 'TE']
                }

    print("1) Testing get_number_of_classes_per_day() function")

    for study_year, tracks in variants.items():
        for track in tracks:
            res = get_number_of_classes_per_day(study_year, track)
            assert res is not None
            assert isinstance(res, dict)
            assert len(res) == 7
            assert all([isinstance(day, str) for day in res.keys()])
            assert all([isinstance(number, int) for number in res.values()])
            assert all([0 <= number for number in res.values()])

        wrong_res = get_number_of_classes_per_day(study_year, 'wrong_track')
        assert wrong_res is None

    print("2) Testing get_free_hours_per_day() function")

    for study_year, tracks in variants.items():
        for track in tracks:
            res = get_free_hours_per_day(study_year, track)
            assert res is not None
            assert isinstance(res, dict)
            assert len(res) == 7
            assert all([isinstance(day, str) for day in res.keys()])
            assert all([isinstance(number, float) for number in res.values()])
            assert all([0 <= number <= 10 for number in res.values()])

        wrong_res = get_free_hours_per_day(study_year, 'wrong_track')
        assert wrong_res is None


def test_for_input():
    print("Running tests for input_handling/input.py")

    print("1) Testing _read_assignments() function")

    assignments = _read_assignments("test-assignments.json")
    print("The following errors are simulated for testing, just ignore them:")
    for assignment in assignments:
        if assignment is None:
            continue

        assert assignment["name"] == "Correct"
        assert isinstance(assignment, dict)
        assert set(assignment.keys()) == {'name', 'start_date', 'end_date', 'hours_to_complete', 'include_weekends'}

        assert isinstance(assignment['name'], str)
        assert isinstance(assignment['start_date'], date)
        assert isinstance(assignment['end_date'], date)
        assert isinstance(assignment['hours_to_complete'], int)
        assert isinstance(assignment['include_weekends'], bool)

        assert assignment['start_date'] <= assignment['end_date']
        assert assignment['hours_to_complete'] > 0

    print("2) Testing _generate_assignments() function")

    # TODO: add more tests for _generate_assignments() function


if __name__ == '__main__':
    print("------------------------------")
    test_get_free_hours()
    print("------------------------------")
    test_for_input()
    print("------------------------------")
    print("All tests passed successfully!")
