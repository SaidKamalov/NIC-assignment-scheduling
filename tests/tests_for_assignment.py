from assignment import Assignment, get_assignments
from datetime import date


def test_assignment():
    print("-" * 20)
    print("Running tests for assignment.py")

    print("1) Testing get_assignments() function")

    assignments = get_assignments("../input_handling/assignments-example.json")
    assert assignments is not None
    assert isinstance(assignments, list)
    for assignment in assignments:
        assert assignment is not None
        assert isinstance(assignment, Assignment)
        assert isinstance(assignment.name, str)
        assert isinstance(assignment.start_date, date)
        assert isinstance(assignment.end_date, date)
        assert isinstance(assignment.hours_to_complete, int)
        assert isinstance(assignment.include_weekends, bool)
        assert assignment.start_date <= assignment.end_date
        assert assignment.hours_to_complete > 0

    assignments = get_assignments(num_of_assignments=10)
    assert assignments is not None
    assert isinstance(assignments, list)
    for assignment in assignments:
        assert assignment is not None
        assert isinstance(assignment, Assignment)
        assert isinstance(assignment.name, str)
        assert isinstance(assignment.start_date, date)
        assert isinstance(assignment.end_date, date)
        assert isinstance(assignment.hours_to_complete, int)
        assert isinstance(assignment.include_weekends, bool)
        assert assignment.start_date <= assignment.end_date
        assert assignment.hours_to_complete > 0


if __name__ == '__main__':
    test_assignment()
