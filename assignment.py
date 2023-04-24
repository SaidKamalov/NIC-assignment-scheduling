from datetime import date


# TODO: to be tested
class Assignment:
    def __init__(
        self,
        name: str,
        start_date: date,
        end_date: date,
        hours_to_complete: int,
        include_weekends: bool,
    ) -> None:
        self.name = name
        self.hours_to_complete = hours_to_complete
        self.include_weekends = include_weekends
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self) -> str:
        res = (
            f"{self.name}: need {self.hours_to_complete} hours to complete\n"
            + f"can be from {self.start_date.year}-{self.start_date.month}-{self.start_date.day} "
            + f"to {self.end_date.year}-{self.end_date.month}-{self.end_date.day}"
        )

        return res


if __name__ == "__main__":
    pass
