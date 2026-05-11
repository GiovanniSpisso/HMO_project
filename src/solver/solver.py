#import csv
import os
import time
from src.io.parser import parse_instance
from src.io.writer import write_solution_file, update_results_csv
from src.heuristics.greedy import greedy
 
def solve_instance(instance_path):
    """
    Main solver entry point.

    Must:
    - print feasible solution lines
    - save each incumbent to a .sol file
    """
    start = time.time()

    m, n, costs, columns = parse_instance(instance_path)
    instance_name = os.path.splitext(os.path.basename(instance_path))[0]

    best_objective = None
    best_columns = None
    solution_count = 1

    # Placeholder: no real heuristic yet, just a dummy solution that takes all columns
    obj, selected = greedy(m, n, costs, columns)
    elapsed = time.time() - start
    
    write_solution_file(instance_path, solution_count, obj, selected, output_dir="solutions/greedy")
    update_results_csv("solutions/greedy/results.csv", instance_name, obj, elapsed)
    
    print("Greedy algorithm:\n")
    print(f"Feasible solution of value {obj} [time {elapsed:.3f}]")