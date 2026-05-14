import argparse
import os
import sys
import time
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.algorithms.pipelines import greedy_local_search, greedy_local_search_2opt
from src.heuristics.greedy import greedy
from src.io.parser import parse_instance
from src.io.saver import make_solution_saver
from src.metaheuristics.ils import ils_hill_climbing, ils_sa
from src.solver.solution_checker import checker, readInstance, readSolution
 
def solve_instance(instance_path):
    """
    Main solver entry point.

    Must:
    - print feasible solution lines
    - save each incumbent to a .sol file
    """

    m, n, costs, columns = parse_instance(instance_path)
    instance_name = os.path.splitext(os.path.basename(instance_path))[0]

    #----------------------PURE GREEDY IMPLEMENTATION-------------------------------
    greedy_saver = make_solution_saver(
        instance_path,
        instance_name,
        "solutions/greedy",
        "solutions/greedy/results.csv",
    )
    start = time.time()
    obj, selected = greedy(
        m,
        n,
        costs,
        columns,
        start_time=start,
        report=True,
        save_solution=greedy_saver,
    )

    #----------------------GREEDY PLUS LOCAL SEARCH-------------------------------------------------
    gls_saver = make_solution_saver(
        instance_path,
        instance_name,
        "solutions/greedy_plus_local_search",
        "solutions/greedy_plus_local_search/results.csv",
    )
    start = time.time()
    obj, selected = greedy_local_search(
        m,
        n,
        costs,
        columns,
        start_time=start,
        report=True,
        save_solution=gls_saver,
    )

    #----------------------GREEDY PLUS LOCAL SEARCH 2-OPT-------------------------------------------------
    gls_2opt_saver = make_solution_saver(
        instance_path,
        instance_name,
        "solutions/greedy_plus_local_search_2opt",
        "solutions/greedy_plus_local_search_2opt/results.csv",
    )
    start = time.time()
    obj, selected = greedy_local_search_2opt(
        m,
        n,
        costs,
        columns,
        start_time=start,
        report=True,
        save_solution=gls_2opt_saver,
    )

    #----------------------ILS + HILL CLIMBING-------------------------------------------------
    ils_hill_climbing_saver = make_solution_saver(
        instance_path,
        instance_name,
        "solutions/ils_hill_climbing",
        "solutions/ils_hill_climbing/results.csv",
    )
    start = time.time()
    obj, selected = ils_hill_climbing(
        m,
        n,
        costs,
        columns,
        num_remove=5,
        random_seed=0,
        max_iter=100,
        start_time=start,
        report=True,
        save_solution=ils_hill_climbing_saver,
    )

    #----------------------ILS + SA-------------------------------------------------
    ils_sa_saver = make_solution_saver(
        instance_path,
        instance_name,
        "solutions/ils_simulated_annealing",
        "solutions/ils_simulated_annealing/results.csv",
    )
    start = time.time()
    obj, selected = ils_sa(
        m,
        n,
        costs,
        columns,
        num_remove=2,
        random_seed=0,
        max_iter=1000,
        initial_temperature=100.0,
        cooling_rate=0.995,
        min_temperature=1e-3,
        start_time=start,
        report=True,
        save_solution=ils_sa_saver,
    )


def check_solution_tree(solutions_root="solutions", instances_root="rail/instances"):
    """Check every .sol file under solutions_root against its matching instance."""

    solutions_root = Path(solutions_root)
    instances_root = Path(instances_root)
    instance_cache = {}

    solution_files = sorted(solutions_root.glob("**/*.sol"))
    if not solution_files:
        print(f"No solution files found under {solutions_root}")
        return

    for solution_path in solution_files:
        instance_name = solution_path.stem.split(".")[0]
        instance_path = instances_root / instance_name

        if not instance_path.exists():
            print(f"Skipping {solution_path}: missing instance file {instance_path}")
            continue

        if instance_name not in instance_cache:
            with instance_path.open("r") as instance_file:
                instance_cache[instance_name] = readInstance(instance_file)

        with solution_path.open("r") as solution_file:
            primal_bound, solution = readSolution(solution_file)

        objective, matrix = instance_cache[instance_name]
        print(f"Checking {solution_path}")
        checker(objective, matrix, primal_bound, solution)


def main():
    parser = argparse.ArgumentParser(description="Run all solvers and validate saved solutions.")
    parser.add_argument("instance_path", help="Path to an ORLIB rail instance file")
    args = parser.parse_args()

    solve_instance(args.instance_path)
    check_solution_tree()


if __name__ == "__main__":
    main()