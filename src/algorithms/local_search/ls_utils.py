"""
Utility functions for local search algorithms.
"""


def build_coverage(m, columns, selected_columns):
    """
    Build a coverage counter for each row of the ground set.
    
    Parameters:
    - m: number of rows
    - columns: list where columns[j] contains rows covered by column j
    - selected_columns: set of selected column indices
    
    Returns:
    - list where coverage[r] is the number of selected columns covering row r
    """
    coverage = [0] * (m + 1)
    
    for j in selected_columns:
        for r in columns[j]:
            coverage[r] += 1
    
    return coverage


def can_remove_column(col_idx, columns, coverage):
    """
    Check if a column can be removed without breaking coverage.
    
    Parameters:
    - col_idx: index of the column to check
    - columns: list where columns[j] contains rows covered by column j
    - coverage: current coverage count for each row
    
    Returns:
    - True if column can be removed, False otherwise
    """
    for r in columns[col_idx]:
        if coverage[r] <= 1:
            return False
    
    return True


def remove_column(col_idx, columns, coverage, selected_set):
    """
    Remove a column from the solution and update coverage.
    
    Parameters:
    - col_idx: index of the column to remove
    - columns: list where columns[j] contains rows covered by column j
    - coverage: current coverage count for each row (will be modified)
    - selected_set: set of selected column indices (will be modified)
    """
    selected_set.remove(col_idx)
    
    for r in columns[col_idx]:
        coverage[r] -= 1
