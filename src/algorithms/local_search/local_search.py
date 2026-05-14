"""
Local search wrapper that applies 0-opt followed by 1-opt cycle.
"""

import time
from src.algorithms.local_search.ls_0opt import local_search_0opt
from src.algorithms.local_search.ls_1opt import local_search_1opt


def local_search(m, costs, columns, selected_columns, start_time=None, 
                report=False, save_solution=None):
    """
    Apply 0-opt + 1-opt cycle until local minimum reached.
    
    First applies 0-opt to remove redundant columns, then applies 1-opt
    to replace columns for improvements. Continues cycling until no more
    improvements are found.
    
    Parameters:
    - m: number of rows
    - costs: list of costs for each column
    - columns: list where columns[j] contains rows covered by column j
    - selected_columns: list of currently selected column indices
    - start_time: time reference for elapsed time calculation
    - report: whether to print progress
    - save_solution: optional callback to save the solution
    
    Returns:
    - (objective_value, selected_columns): tuple with total cost and list of selected column indices
    """
    if start_time is None:
        start_time = time.time()
    
    best_obj = sum(costs[j] for j in selected_columns)
    best_selected = list(selected_columns)
    
    improved = True
    
    while improved:
        improved = False
        
        # Apply 0-opt
        obj_0opt, selected_0opt = local_search_0opt(
            m, costs, columns, best_selected,
            start_time=start_time, report=False
        )
        
        if obj_0opt < best_obj:
            best_obj = obj_0opt
            best_selected = selected_0opt
            improved = True
            
            if report:
                elapsed = time.time() - start_time
                print(f"Feasible solution of value {best_obj} [time {elapsed:.3f}]")
                if save_solution is not None:
                    try:
                        save_solution(best_obj, best_selected, elapsed)
                    except TypeError:
                        save_solution(best_obj, best_selected)
        
        # Apply 1-opt
        obj_1opt, selected_1opt = local_search_1opt(
            m, costs, columns, best_selected,
            start_time=start_time, report=False
        )
        
        if obj_1opt < best_obj:
            best_obj = obj_1opt
            best_selected = selected_1opt
            improved = True
            
            if report:
                elapsed = time.time() - start_time
                print(f"Feasible solution of value {best_obj} [time {elapsed:.3f}]")
                if save_solution is not None:
                    try:
                        save_solution(best_obj, best_selected, elapsed)
                    except TypeError:
                        save_solution(best_obj, best_selected)
    
    elapsed = time.time() - start_time
    
    if report:
        print(f"Feasible solution of value {best_obj} [time {elapsed:.3f}]")
    
    if report and save_solution is not None:
        try:
            save_solution(best_obj, best_selected, elapsed)
        except TypeError:
            save_solution(best_obj, best_selected)
    
    return best_obj, best_selected
