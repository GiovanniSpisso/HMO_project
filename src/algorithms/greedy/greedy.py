"""
Greedy algorithm for the Set Covering Problem.

This is a general greedy implementation that can start from scratch
or from a partial solution.
"""

import time
from src.algorithms.greedy.greedy_utils import convert_to_sets


def greedy_from_scratch(m, n, costs, columns, start_time=None, report=False, save_solution=None):
    """
    Greedy column selection from scratch.
    
    Starts with an empty solution and greedily adds columns until all rows are covered.
    
    Parameters:
    - m: number of rows
    - n: number of columns
    - costs: list of costs for each column
    - columns: list where columns[j] contains rows covered by column j
    - start_time: time reference for elapsed time calculation
    - report: whether to print progress
    - save_solution: optional callback to save the solution
    
    Returns:
    - (objective_value, selected_columns): tuple with total cost and list of selected column indices
    """
    if start_time is None:
        start_time = time.time()
    
    # Ground set uncovered elements
    uncovered = set(range(1, m + 1))
    
    # Used to store the chosen subset (i.e. columns)
    selected_columns = []
    objective_value = 0
    
    # Convert once to sets (much faster)
    column_sets = convert_to_sets(columns)
    
    # Columns not yet selected
    available_columns = set(range(n))
    
    while uncovered:
        best_col = None
        best_ratio = float("inf")
        best_new_rows = set()
        
        for j in available_columns:
            new_rows = uncovered & column_sets[j]
            
            if not new_rows:
                continue
            
            ratio = costs[j] / len(new_rows)
            
            if ratio < best_ratio:
                best_ratio = ratio
                best_col = j
                best_new_rows = new_rows
        
        if best_col is None:
            raise RuntimeError("No feasible solution found.")
        
        # select column
        selected_columns.append(best_col)
        objective_value += costs[best_col]
        
        # update uncovered rows
        uncovered -= best_new_rows
        
        # remove selected column
        available_columns.remove(best_col)
    
    elapsed = time.time() - start_time
    
    if report:
        print(f"Feasible solution of value {objective_value} [time {elapsed:.3f}]")
    
    if report and save_solution is not None:
        try:
            save_solution(objective_value, selected_columns, elapsed)
        except TypeError:
            save_solution(objective_value, selected_columns)
    
    return objective_value, selected_columns


def greedy_from_partial(m, n, costs, columns, partial_selected, partial_objective_value, 
                        start_time=None, report=False, save_solution=None):
    """
    Greedy column selection starting from a partial solution.
    
    Continues greedily adding columns to cover uncovered rows,
    starting from the given partial solution.
    
    Parameters:
    - m: number of rows
    - n: number of columns
    - costs: list of costs for each column
    - columns: list where columns[j] contains rows covered by column j
    - partial_selected: set of column indices already selected
    - partial_objective_value: objective value of the partial selection
    - start_time: time reference for elapsed time calculation
    - report: whether to print progress
    - save_solution: optional callback to save the solution
    
    Returns:
    - (objective_value, selected_columns): tuple with total cost and list of selected column indices
    """
    if start_time is None:
        start_time = time.time()
    
    # Ground set uncovered elements
    uncovered = set(range(1, m + 1))
    
    # Start with the partial solution
    selected_columns = list(partial_selected)
    objective_value = partial_objective_value
    
    # Convert once to sets (much faster)
    column_sets = convert_to_sets(columns)
    
    # Remove rows already covered by partial solution
    for j in partial_selected:
        uncovered -= column_sets[j]
    
    # Columns not yet selected
    available_columns = set(range(n)) - partial_selected
    
    while uncovered:
        best_col = None
        best_ratio = float("inf")
        best_new_rows = set()
        
        for j in available_columns:
            new_rows = uncovered & column_sets[j]
            
            if not new_rows:
                continue
            
            ratio = costs[j] / len(new_rows)
            
            if ratio < best_ratio:
                best_ratio = ratio
                best_col = j
                best_new_rows = new_rows
        
        if best_col is None:
            raise RuntimeError("No feasible solution found.")
        
        # select column
        selected_columns.append(best_col)
        objective_value += costs[best_col]
        
        # update uncovered rows
        uncovered -= best_new_rows
        
        # remove selected column
        available_columns.remove(best_col)
    
    elapsed = time.time() - start_time
    
    if report:
        print(f"Feasible solution of value {objective_value} [time {elapsed:.3f}]")
    
    if report and save_solution is not None:
        try:
            save_solution(objective_value, selected_columns, elapsed)
        except TypeError:
            save_solution(objective_value, selected_columns)
    
    return objective_value, selected_columns
