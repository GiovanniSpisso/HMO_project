#import csv
import os
import time
from src.io.parser import parse_instance
from src.io.writer import write_solution_file, update_results_csv
from src.heuristics.greedy import greedy
from src.heuristics.construction import greedy_local_search
 
def solve_instance(instance_path):
    """
    Main solver entry point.

    Must:
    - print feasible solution lines
    - save each incumbent to a .sol file
    """

    m, n, costs, columns = parse_instance(instance_path)
    instance_name = os.path.splitext(os.path.basename(instance_path))[0]

    #best_objective = None
    #best_columns = None
    solution_count = 1

    #----------------------PURE GREEDY IMPLEMENTATION-------------------------------
    start = time.time()
    obj, selected = greedy(m, n, costs, columns)
    elapsed = time.time() - start
    
    write_solution_file(instance_path, solution_count, obj, selected, output_dir="solutions/greedy")
    update_results_csv("solutions/greedy/results.csv", instance_name, obj, elapsed)
    
    print("Greedy algorithm:")
    print(f"Feasible solution of value {obj} [time {elapsed:.3f}]\n")

    #----------------------GREEDY PLUS LOCAL SEARCH-------------------------------------------------
    start = time.time()
    obj, selected = greedy_local_search(m, n, costs, columns)
    elapsed = time.time() - start

    write_solution_file(instance_path, solution_count, obj, selected, output_dir="solutions/greedy_plus_local_search")
    update_results_csv("solutions/greedy_plus_local_search/results.csv", instance_name, obj, elapsed)

    print("Greedy plus local search:")
    print(f"Feasible solution of value {obj} [time {elapsed:.3f}]\n")