import json
from datetime import date


def get_assignments(path_to_json: str, random: bool = False):
    if random:  # TODO call function that creates random assignments for testing
        pass
    else:
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


if __name__ == "__main__":
    # TODO: remove later, just for test
    for ass in get_assignments("./input-handling/assignments-example.json"):
        print(ass)
