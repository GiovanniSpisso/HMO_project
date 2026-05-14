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
from src.algorithms.greedy.greedy import greedy_from_scratch
from src.algorithms.local_search.local_search import local_search
from src.algorithms.perturb.perturb import perturb
from src.algorithms.acceptance_criteria.accept_hc import accept_hill_climbing
from src.algorithms.acceptance_criteria.accept_sa import accept_simulated_annealing
from src.algorithms.greedy.greedy import greedy_from_partial
from src.solver.solution_checker import checker, readInstance, readSolution


def solve_instance(instance_path, max_total_time=300, hc_time_limit=120, 
                  num_remove=5, random_seed=0, consecutive_no_improve=100):
    """
    Comprehensive solver orchestrator for the Set Covering Problem.
    
    Performs the following sequence:
    1. Greedy from scratch
    2. Local search (0-opt + 1-opt cycle) until local minimum
    3. ILS loop:
       - Perturb: remove N random columns
       - Local search: apply 0-opt + 1-opt
       - Acceptance: use Hill Climbing if in HC phase, else Simulated Annealing
    
    Parameters:
    - instance_path: path to the instance file
    - max_total_time: maximum total time in seconds 
    - hc_time_limit: time limit for Hill Climbing phase in seconds 
    - num_remove: number of columns to remove during perturbation
    - random_seed: seed for reproducibility
    - consecutive_no_improve: iterations without improvement to stop HC early
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
    
    # Phase 1: Greedy from scratch
    best_obj, best_selected = greedy_from_scratch(
        m, n, costs, columns,
        start_time=global_start,
        report=True,
        save_solution=saver,
    )
    
    # Phase 2: Local search (0-opt + 1-opt cycle)
    best_obj, best_selected = local_search(
        m, costs, columns, best_selected,
        start_time=global_start,
        report=True,
        save_solution=saver,
    )
    
    # Phase 3: ILS loop
    consecutive_no_improve_count = 0
    iteration = 0
    temperature = 100.0
    
    while True:
        elapsed = time.time() - global_start
        
        # Check total time limit
        if elapsed >= max_total_time:
            break
        
        # Determine which phase we're in
        in_hc_phase = (elapsed < hc_time_limit and 
                      consecutive_no_improve_count < consecutive_no_improve)
        
        # --- PERTURBATION: Remove N random columns ---
        remaining_selected, removal_set = perturb(best_selected, num_remove)
        
        # --- REPAIR: Greedy construction from remaining columns ---
        removed_cost = sum(costs[j] for j in removal_set)
        remaining_objective = best_obj - removed_cost
        
        obj_repaired, selected_repaired = greedy_from_partial(
            m, n, costs, columns, remaining_selected, remaining_objective,
            start_time=global_start, report=False
        )
        
        # --- LOCAL SEARCH: Apply 0-opt + 1-opt cycle ---
        obj_candidate, selected_candidate = local_search(
            m, costs, columns, selected_repaired,
            start_time=global_start, report=False
        )
        
        # --- ACCEPTANCE: Determine if we accept this solution ---
        accept = False
        
        if in_hc_phase:
            # Hill Climbing: accept only if improves best
            accept = accept_hill_climbing(obj_candidate, best_obj)
            
            if not accept:
                consecutive_no_improve_count += 1
        else:
            # Simulated Annealing: probabilistic acceptance
            accept = accept_simulated_annealing(obj_candidate, best_obj, temperature)
            temperature *= 0.995  # Cool down
        
        # Update best solution if candidate is better
        if obj_candidate < best_obj:
            best_obj = obj_candidate
            best_selected = selected_candidate
            consecutive_no_improve_count = 0
            
            elapsed = time.time() - global_start
            print(f"Feasible solution of value {best_obj} [time {elapsed:.3f}]")
            saver(best_obj, best_selected, elapsed)
        
        iteration += 1


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
    parser = argparse.ArgumentParser(description="Comprehensive solver for Set Covering Problem.")
    parser.add_argument("instance_path", help="Path to an ORLIB rail instance file")
    parser.add_argument("--max-time", type=int, default=600,
                       help="Maximum total time in seconds (default: 600)")
    parser.add_argument("--hc-time", type=int, default=180,
                       help="Time limit for Hill Climbing phase in seconds (default: 180)")
    parser.add_argument("--num-remove", type=int, default=5,
                       help="Number of columns to remove in ILS perturbation (default: 5)")
    parser.add_argument("--random-seed", type=int, default=0,
                       help="Random seed for reproducibility (default: 0)")
    parser.add_argument("--no-improve-limit", type=int, default=100,
                       help="Consecutive iterations without improvement to stop HC (default: 100)")
    
    args = parser.parse_args()

    solve_instance(
        args.instance_path,
        max_total_time=args.max_time,
        hc_time_limit=args.hc_time,
        num_remove=args.num_remove,
        random_seed=args.random_seed,
        consecutive_no_improve=args.no_improve_limit,
    )
    check_solution_tree()


if __name__ == "__main__":
    main()