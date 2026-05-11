def build_coverage(m, columns, selected_columns):
    """
    Build a coverage counter for each row of the ground set.

    For each row r, coverage[r] indicates how many selected columns
    currently cover that row.

    This structure is useful in local search procedures to:
    - quickly check feasibility when removing a column
    - avoid recomputing full coverage from scratch
    - support efficient incremental updates

    Parameters:
    - m: number of rows in the ground set (rows are 1-based indexed)
    - columns: list of sets/lists, where columns[j] contains the rows
               covered by column j
    - selected_columns: list of indices of currently selected columns

    Returns:
    - coverage: list where coverage[r] = number of selected columns
                that cover row r (index 0 is unused)
    """

    coverage = [0] * (m + 1)

    for j in selected_columns:
        for r in columns[j]:
            coverage[r] += 1

    return coverage

def can_remove_column(col_idx, columns, coverage):
    """
    Check whether a column can be safely removed from the current solution
    without violating feasibility.

    A column is removable if all the rows it covers are still covered
    by at least one other selected column.

    In practice, for every row r covered by this column, we require:
        coverage[r] > 1
    meaning that at least one additional selected column also covers r.

    Parameters:
    - col_idx: index of the column to test for removal
    - columns: list of sets/lists where columns[j] contains the rows
               covered by column j
    - coverage: list where coverage[r] is the number of selected columns
                currently covering row r

    Returns:
    - True if the column can be removed safely
    - False otherwise
    """

    for r in columns[col_idx]:
        if coverage[r] <= 1:
            return False

    return True

def remove_column(col_idx, columns, coverage, selected_set):
    """
    Remove a column from the current solution and update the coverage structure.

    This function assumes that the removal is feasible (i.e., it has already been
    checked using can_remove_column). It updates both:
    - the set of selected columns
    - the coverage counters for each row

    Parameters:
    - col_idx: index of the column to remove
    - columns: list of sets/lists where columns[j] contains the rows
               covered by column j
    - coverage: list where coverage[r] counts how many selected columns
                currently cover row r
    - selected_set: set of currently selected column indices (will be modified)

    Returns:
    - None (modifies selected_set and coverage in place)
    """

    selected_set.remove(col_idx)

    for r in columns[col_idx]:
        coverage[r] -= 1


def local_search_remove(m, costs, columns, selected_columns):
    """
    Perform a simple improvement local search for the Set Covering Problem.

    Starting from a feasible solution (typically produced by greedy),
    this procedure iteratively removes redundant columns while preserving
    feasibility.

    The idea is a 1-opt neighborhood:
    - try to remove one selected column at a time
    - keep it removed only if all rows remain covered
    - repeat until no further improvement is possible

    Parameters:
    - m: number of rows in the ground set
    - costs: list of costs associated with each column
    - columns: list where columns[j] contains the rows covered by column j
    - selected_columns: initial feasible solution (list of column indices)

    Returns:
    - objective_value: total cost of the improved solution
    - selected_columns: improved list of selected columns (sorted)
    """

    selected_set = set(selected_columns)

    # Build initial coverage (how many selected columns cover each row)
    coverage = build_coverage(m, columns, selected_set)

    improved = True

    # Repeat until no more columns can be removed
    while improved:

        improved = False

        # Iterate over a copy since we may modify the set during iteration
        for j in list(selected_set):

            if can_remove_column(j, columns, coverage):

                remove_column(j, columns, coverage, selected_set)

                improved = True

    selected_columns = sorted(selected_set)

    # Recompute objective value of final solution
    objective_value = sum(costs[j] for j in selected_columns)

    return objective_value, selected_columns