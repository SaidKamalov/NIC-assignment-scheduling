from schedule import Schedule
from datetime import date
from collections import OrderedDict


def test_schedule():
    print('-' * 20)
    print('Running tests for schedule.py')

    print('1) Testing Schedule class')
    schedule = Schedule()
    assert schedule is not None
    assert isinstance(schedule, Schedule)
    assert schedule.start is not None
    assert schedule.end is not None
    assert schedule.days is not None
    assert isinstance(schedule.start, date)
    assert isinstance(schedule.end, date)
    assert isinstance(schedule.days, OrderedDict)
    assert schedule.start <= schedule.end
    assert len(schedule.days) > 0
    for day, free_hours in schedule.days.items():
        assert day is not None
        assert isinstance(day, date)
        assert free_hours is not None
        assert isinstance(free_hours, float)
        assert free_hours >= 0.0
        assert free_hours <= 24.0

    print('2) Testing get_free_time() method')
    from_ = date(2021, 9, 1)
    to = date(2021, 9, 30)
    free_hours = schedule.get_free_time(from_, to)
    assert free_hours is not None
    assert isinstance(free_hours, float)
    assert free_hours >= 0.0


if __name__ == '__main__':
    test_schedule()
