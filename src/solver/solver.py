#import csv
import os
import time
from src.io.parser import parse_instance
from src.io.saver import make_solution_saver
from src.heuristics.greedy import greedy
from src.algorithms.pipelines import greedy_local_search, greedy_local_search_2opt
from src.metaheuristics.ils import ils
 
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
    ils_saver = make_solution_saver(
        instance_path,
        instance_name,
        "solutions/ils_hill_climbing",
        "solutions/ils_hill_climbing/results.csv",
    )
    start = time.time()
    obj, selected = ils(
        m,
        n,
        costs,
        columns,
        num_remove=5,
        random_seed=0,
        max_iter=100,
        start_time=start,
        report=True,
        save_solution=ils_saver,
    )