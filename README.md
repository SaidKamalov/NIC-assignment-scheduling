<h1 align="center"> NIC-assignment-scheduling</h1>

From year to year, students and teachers face the problem of Assignments Scheduling. Overlapping assignments may cause
such problems as burnout, underestimated results, and unwanted but inevitable deadline extensions. Therefore, our team
decided to try to solve this issue with the help of Nature Inspired Computing.

## The structure of the project

- `input_handling` - contains the code for reading the input data
- `tests` - contains the tests for the input data
- `assignment.py` - contains the code for the Assignment class
- `schedule.py` - contains the code for the Schedule class
- `genetic_algorithm.py` - contains the code for the generic Genetic Algorithm
- `domain_to_ga.py` - contains the code for converting our domain to the GA domain
- `environment.py` - contains the configuration of the project
- `experiments.py` - contains the code for visualization of the solutions
- `requirements.txt` - contains the list of all the dependencies

## Assignments Format

The input data is represented as json file with the list of `assignments`, each described with:

- `name: str` - the name of the assignment
- `start_date: date` - the date when the assignment can be started
- `end_date: date` - the date when the assignment should be finished
- `hours_to_complete: int` - the number of hours needed to complete the assignment
- `include_weekends: bool` - whether the assignment can be done on weekends

Constraints:

- `start_date` < `end_date`
- `hours_to_complete` > 0

The example of the input data can be found in [`input_handling/assignments-example.json`](https://github.com/SaidKamalov/NIC-assignment-scheduling/blob/main/input_handling/assignments-example.json).

## Schedule Format

The students' schedule is represented as json file and has the following structure:

- `Study Year`: {
    - `Study Track`: {
        - `0`: number of classes on Monday
        - ...
        - `6`: number of classes on Sunday
          }
          }

The example of the schedule can be found in [`input_handling/schedule-example.json`](https://github.com/SaidKamalov/NIC-assignment-scheduling/blob/main/input_handling/schedule-example.json).

## How to run the project

1. Clone the repository
2. Install the dependencies with 
```bash
pip install -r requirements.txt
```
3. Configure the algorithm parameters in `environment.py`
4. Run the project with 
```bash
python genetic_algorithm.py
```
To run the tests, use 
```bash
python tests/test_all.py
```

## How to use Genetic Algorithm for your own problem

The genetic algorithm is implemented in `genetic_algorithm.py`. To use it for your own problem, you need to implement
the following:

- `Gene` class, which represents the gene of the chromosome
- `Chromosome` class, which represents the chromosome
- `fitness` function, which calculates the fitness of the chromosome
- `crossover` function, which performs crossover of two chromosomes
- `mutation` function, which performs mutation of the chromosome
- `generation` function, which generates the new chromosomes

You can use the default implementation of functions if it is suitable.

## Authors

- [Said Kamalov](https://github.com/SaidKamalov)
- [Lev Rekhlov](https://github.com/plov-cyber)
- [Karina Denisova](https://github.com/karinaDen)

