"""
0-opt local search for the Set Covering Problem.

This algorithm removes redundant columns (columns that don't break coverage)
until no more can be removed.
"""

import time
from src.algorithms.local_search.ls_utils import (
    build_coverage, 
    can_remove_column, 
    remove_column
)


def local_search_0opt(m, costs, columns, selected_columns, start_time=None, 
                     report=False, save_solution=None):
    """
    0-opt local search: remove redundant columns.
    
    Iteratively removes columns that don't break coverage (columns where
    all covered rows are covered by at least one other selected column)
    until no more columns can be removed.
    
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
    
    selected_set = set(selected_columns)
    coverage = build_coverage(m, columns, selected_set)
    current_cost = sum(costs[j] for j in selected_set)
    
    improved = True
    
    while improved:
        improved = False
        
        for j in list(selected_set):
            if can_remove_column(j, columns, coverage):
                remove_column(j, columns, coverage, selected_set)
                current_cost -= costs[j]
                
                improved = True
                
                if report:
                    elapsed = time.time() - start_time
                    print(f"Feasible solution of value {current_cost} [time {elapsed:.3f}]")
                    if save_solution is not None:
                        try:
                            save_solution(current_cost, sorted(selected_set), elapsed)
                        except TypeError:
                            save_solution(current_cost, sorted(selected_set))
                
                break
    
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
