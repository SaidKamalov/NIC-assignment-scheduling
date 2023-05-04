from tests_for_assignment import test_assignment
from tests_for_input_handling import test_input, test_get_free_hours
from tests_for_schedule import test_schedule
from tests_for_ga import test_genetic_algorithm

if __name__ == '__main__':
    test_input()
    test_get_free_hours()
    test_assignment()
    test_schedule()
    test_genetic_algorithm()
    print("-" * 20)
    print("All tests were passed successfully!")
