import argparse
import os
import sys
import time
import random
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.io.parser import parse_instance
from src.io.saver import make_solution_saver
from src.algorithms.greedy.greedy import greedy_from_partial, greedy_from_scratch
from src.algorithms.local_search.local_search import local_search
from src.algorithms.perturb.perturb import perturb
from src.algorithms.acceptance_criteria.accept_hc import accept_hill_climbing
from src.solver.solution_checker import checker, readInstance, readSolution


def solve_instance(instance_path, max_total_time=60, 
                   random_seed=0, perc_remove=10, 
                   hc_time_limit=60):
    """
    Comprehensive solver orchestrator for the Set Covering Problem.
    
    Performs the following sequence:
    1. Greedy from scratch
    2. Local search (0-opt cycle) until local minimum
    3. ILS loop:
         - Perturb: remove random columns, then add random columns until feasibility is restored
         - Local search (0-opt cycle) until local minimum
         - Acceptance: use Hill Climbing
    
    Parameters:
    - instance_path: path to the instance file
    - max_total_time: maximum total time in seconds 
    - random_seed: seed for reproducibility
    - perc_remove: percentage of random columns to remove during perturbation
    - hc_time_limit: time limit for Hill Climbing phase in seconds 
    """
    
    m, n, costs, columns = parse_instance(instance_path)
    instance_name = os.path.splitext(os.path.basename(instance_path))[0]
    
    # Create solution saver
    saver = make_solution_saver(
        instance_path,
        instance_name,
        "solutions",
        "solutions/results.csv",
    )
    
    global_start = time.time()
    
    # Set random seed once at the start
    if random_seed is not None:
        random.seed(random_seed)

    print("-----------------------------------------------")
    print(f"Greedy starting at time {(time.time() - global_start):.3f}")
    print("-----------------------------------------------")

    # Phase 1: Greedy from scratch
    best_obj, best_selected = greedy_from_scratch(
        m, n, costs, columns,
        start_time=global_start,
        report=True,
        save_solution=saver,
    )

    print("-----------------------------------------------")
    print(f"Greedy ending at time {(time.time() - global_start):.3f}")
    print("-----------------------------------------------")
    
    print("-----------------------------------------------")
    print(f"Local search starting at time {(time.time() - global_start):.3f}")
    print("-----------------------------------------------")
    # Phase 2: Local search (0-opt cycle)
    best_obj, best_selected = local_search(
        m, costs, columns, best_selected,
        start_obj = best_obj,
        start_time=global_start,
        report=True,
        save_solution=saver,
    )
    print("-----------------------------------------------")
    print(f"Local search ending at time {(time.time() - global_start):.3f}")
    print("-----------------------------------------------")
    
    print("-----------------------------------------------")
    print(f"Hill climbing starting at time {(time.time() - global_start):.3f}")
    print("-----------------------------------------------")
    # Phase 3: ILS loop
    consecutive_no_improve_count = 0
    iteration = 0
    
    while True:
        elapsed = time.time() - global_start
        
        # Check total time limit
        if elapsed >= max_total_time:
            break
        
        # --- PERTURBATION: Remove N random columns ---
        num_remove = int(len(best_selected) * perc_remove / 100)
        remaining_selected, removal_set = perturb(best_selected, num_remove)
        
        # --- REPAIR: Greedy construction from remaining columns ---
        removed_cost = sum(costs[j] for j in removal_set)
        remaining_objective = best_obj - removed_cost
        
        obj_repaired, selected_repaired = greedy_from_partial(
            m, n, costs, columns, remaining_selected, remaining_objective,
            start_time=global_start, report=False
        )

        # --- LOCAL SEARCH: Apply 0-opt cycle ---
        obj_candidate, selected_candidate = local_search(
            m, costs, columns, selected_repaired,
            start_obj = obj_repaired, start_time=global_start, report=True
        )
        
        # --- ACCEPTANCE: Determine if we accept this solution ---
        accept = False
        
        # Hill Climbing: accept only if improves best
        accept = accept_hill_climbing(obj_candidate, best_obj)
        
        if not accept:
            consecutive_no_improve_count += 1
        else:
            consecutive_no_improve_count = 0
        
        if elapsed > hc_time_limit: 
            print("Stopping Hill Climbing phase due to time limit.")
            print("-----------------------------------------------")
            print(f"Hill climbing ending at time {(time.time() - global_start):.3f} with {iteration} number of iterations")
            print("-----------------------------------------------")
        
        # Update best solution if accept is true ==> current for the moment because we want to print also the negative improvements in this phase of the project
        if accept:
            best_obj = obj_candidate
            best_selected = selected_candidate
            
            elapsed = time.time() - global_start
            print(f"Feasible solution of value {best_obj} [time {elapsed:.3f}] (iteration {iteration})")
            saver(best_obj, best_selected, elapsed)
        
        iteration += 1
    
    return instance_name


def check_solution_tree(solutions_root="solutions", instances_root="rail/instances", instance_name=None):
    """Check .sol files under solutions_root against their matching instances.
    
    If instance_name is provided, only check solutions for that specific instance.
    Otherwise, check all solutions for all instances.
    """

    solutions_root = Path(solutions_root)
    instances_root = Path(instances_root)
    instance_cache = {}

    def solution_sort_key(path: Path):
        parts = path.stem.split(".")
        base_name = parts[0]
        if len(parts) > 1 and parts[1].isdigit():
            return (base_name, 0, int(parts[1]))
        if len(parts) > 1:
            return (base_name, 1, parts[1])
        return (base_name, 2, "")

    solution_files = sorted(solutions_root.glob("**/*.sol"), key=solution_sort_key)
    if not solution_files:
        print(f"No solution files found under {solutions_root}")
        return
    
    # Filter solutions by instance_name if provided
    if instance_name:
        solution_files = [f for f in solution_files if f.stem.split(".")[0] == instance_name]
        solution_files = sorted(solution_files, key=solution_sort_key)
        if not solution_files:
            print(f"No solution files found for instance {instance_name}")
            return

    for solution_path in solution_files:
        stem_parts = solution_path.stem.split(".")
        instance_name = stem_parts[0]
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
    parser = argparse.ArgumentParser(description="Comprehensive solver for Set Covering Problem.")
    parser.add_argument("instance_path", help="Path to an ORLIB rail instance file")
    parser.add_argument("--max-time", type=int, default=600,
                       help="Maximum total time in seconds (default: 600)")
    parser.add_argument("--hc-time", type=int, default=180,
                       help="Time limit for Hill Climbing phase in seconds (default: 120)")
    parser.add_argument("--num-remove", type=int, default=5,
                       help="Number of random columns to remove before feasibility repair (default: 5)")
    parser.add_argument("--random-seed", type=int, default=0,
                       help="Random seed for reproducibility (default: 0)")
    args = parser.parse_args()

    solve_instance(
        args.instance_path,
        max_total_time=args.max_time,
        hc_time_limit=args.hc_time,
        perc_remove=args.num_remove,
        random_seed=args.random_seed,
    )
    instance_name = os.path.splitext(os.path.basename(args.instance_path))[0]
    check_solution_tree(instance_name=instance_name)


if __name__ == "__main__":
    main()