from input_handling.input import _read_assignments, _generate_assignments, get_free_hours_per_day, \
    get_number_of_classes_per_day
from datetime import date, timedelta

PATH = "../input_handling/inno_number_of_classes.json"


def test_get_free_hours():
    print("-" * 20)
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
            res = get_number_of_classes_per_day(study_year, track, PATH)
            assert res is not None
            assert isinstance(res, dict)
            assert len(res) == 7
            assert all([isinstance(day, str) for day in res.keys()])
            assert all([isinstance(number, int) for number in res.values()])
            assert all([0 <= number for number in res.values()])

        wrong_res = get_number_of_classes_per_day(study_year, 'wrong_track', PATH)
        assert wrong_res is None

    print("2) Testing get_free_hours_per_day() function")

    for study_year, tracks in variants.items():
        for track in tracks:
            res = get_free_hours_per_day(study_year, track, PATH)
            assert res is not None
            assert isinstance(res, dict)
            assert len(res) == 7
            assert all([isinstance(day, str) for day in res.keys()])
            assert all([isinstance(number, float) for number in res.values()])
            assert all([0 <= number <= 10 for number in res.values()])

        wrong_res = get_free_hours_per_day(study_year, 'wrong_track', PATH)
        assert wrong_res is None


def test_input():
    print("-" * 20)
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

    correct_tests = [
        {"num_of_assignments": 1,
         "max_day_range": 1,
         "min_day_range": 1,
         "working_hours_ratio": 1,
         "include_weekends_prob": 1},
        {"num_of_assignments": 10,
         "max_day_range": 10,
         "min_day_range": 1,
         "working_hours_ratio": 0.001,
         "include_weekends_prob": 0.001},
        {"num_of_assignments": 100,
         "max_day_range": 100,
         "min_day_range": 1,
         "working_hours_ratio": 0.999,
         "include_weekends_prob": 0.283},
        {"num_of_assignments": 1000,
         "max_day_range": 30,
         "min_day_range": 30,
         "working_hours_ratio": 0.228,
         "include_weekends_prob": 0.01},
    ]
    wrong_tests = [
        {"num_of_assignments": 0,
         "max_day_range": 1,
         "min_day_range": 1,
         "working_hours_ratio": 1,
         "include_weekends_prob": 1},
        {"num_of_assignments": 1,
         "max_day_range": 0,
         "min_day_range": 1,
         "working_hours_ratio": 1,
         "include_weekends_prob": 1},
        {"num_of_assignments": 1,
         "max_day_range": 1,
         "min_day_range": 0,
         "working_hours_ratio": 1,
         "include_weekends_prob": 1},
        {"num_of_assignments": 1,
         "max_day_range": 1,
         "min_day_range": 1,
         "working_hours_ratio": -1,
         "include_weekends_prob": 1},
        {"num_of_assignments": 1,
         "max_day_range": 1,
         "min_day_range": 1,
         "working_hours_ratio": 1,
         "include_weekends_prob": -1},
        {"num_of_assignments": 1,
         "max_day_range": 1,
         "min_day_range": 1,
         "working_hours_ratio": 2,
         "include_weekends_prob": 1},
        {"num_of_assignments": 1,
         "max_day_range": 1,
         "min_day_range": 1,
         "working_hours_ratio": 1,
         "include_weekends_prob": 2}
    ]

    for test in correct_tests:
        assignments = _generate_assignments(**test)
        assert assignments is not None
        assignment_cnt = 0
        for assignment in assignments:
            assert assignment is not None
            assert isinstance(assignment, dict)
            assert set(assignment.keys()) == {'name', 'start_date', 'end_date', 'hours_to_complete', 'include_weekends'}

            assert isinstance(assignment['name'], str)
            assert isinstance(assignment['start_date'], date)
            assert isinstance(assignment['end_date'], date)
            assert isinstance(assignment['hours_to_complete'], int)
            assert isinstance(assignment['include_weekends'], bool)

            assert assignment['start_date'] <= assignment['end_date']
            assert assignment['hours_to_complete'] > 0
            assert assignment['end_date'] - assignment['start_date'] <= timedelta(days=test["max_day_range"])
            assert assignment['end_date'] - assignment['start_date'] >= timedelta(days=test["min_day_range"])
            assert 0 <= assignment['hours_to_complete']
            assignment_cnt += 1
        assert assignment_cnt == test["num_of_assignments"]

    print("The following errors are simulated for testing, just ignore them:")
    for test in wrong_tests:
        assignments = _generate_assignments(**test)
        for assignment in assignments:
            assert assignment is None


if __name__ == '__main__':
    test_get_free_hours()
    test_input()
