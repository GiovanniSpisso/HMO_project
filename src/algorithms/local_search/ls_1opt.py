"""
1-opt local search for the Set Covering Problem.

This algorithm tries to replace one selected column with one alternative,
STOPPING on the first improvement found.
"""

import time
from src.algorithms.local_search.ls_utils import build_coverage


def local_search_1opt(m, costs, columns, selected_columns, start_obj=None,
                      start_time=None, report=False, save_solution=None):
    """
    1-opt local search: replace 1 selected column with 1 unselected column.
    
    Tries to improve the solution by replacing a selected column with a single
    unselected column that keeps the solution feasible and reduces the cost.
    Stops and returns immediately upon finding the first improvement.
    
    Parameters:
    - m: number of rows
    - costs: list of costs for each column
    - columns: list where columns[j] contains rows covered by column j
    - selected_columns: list of currently selected column indices
    - start_obj: initial objective of input solution
    - start_time: time reference for elapsed time calculation
    - report: whether to print progress
    - save_solution: optional callback to save the solution
    
    Returns:
    - (objective_value, selected_columns): tuple with total cost and list of selected column indices
    """
    if start_time is None:
        start_time = time.time()
    
    selected_set = set(selected_columns)
    coverage = build_coverage(m, columns, selected_set)
    if start_obj is None:
        current_cost = sum(costs[j] for j in selected_set)
    else:
        current_cost = start_obj
    
    improved = True
    
    while improved:
        improved = False
        
        for j_remove in list(selected_set):
            remove_cost = costs[j_remove]
            
            # Find rows that would be uncovered if we remove this column
            uncovered_after_removal = set()
            for r in columns[j_remove]:
                if coverage[r] <= 1:
                    uncovered_after_removal.add(r)
            
            # Try to find a replacement column that covers all uncovered rows
            best_replacement = None
            best_replacement_cost = remove_cost
            
            for j_add in range(len(columns)):
                if j_add in selected_set:
                    continue
                
                if uncovered_after_removal.issubset(set(columns[j_add])):
                    replacement_cost = costs[j_add]
                    if replacement_cost < best_replacement_cost:
                        best_replacement_cost = replacement_cost
                        best_replacement = j_add
            
            # If we found an improvement, apply it and stop
            if best_replacement is not None:
                selected_set.remove(j_remove)
                for r in columns[j_remove]:
                    coverage[r] -= 1
                
                selected_set.add(best_replacement)
                for r in columns[best_replacement]:
                    coverage[r] += 1
                
                current_cost += best_replacement_cost - remove_cost
                improved = True
                
                if report:
                    elapsed = time.time() - start_time
                    print(f"Feasible solution of value {current_cost} [time {elapsed:.3f}]")
                    if save_solution is not None:
                        try:
                            save_solution(current_cost, sorted(selected_set), elapsed)
                        except TypeError:
                            save_solution(current_cost, sorted(selected_set))
                
                break  # Stop on first improvement
    
    selected_columns = sorted(selected_set)
    elapsed = time.time() - start_time
    
    if report:
        print(f"Feasible solution of value {current_cost} [time {elapsed:.3f}]")
    
    if report and save_solution is not None:
        try:
            save_solution(current_cost, selected_columns, elapsed)
        except TypeError:
            save_solution(current_cost, selected_columns)
    
    return current_cost, selected_columns
