"""
Perturbation function for ILS: removes random columns, then adds random columns until feasible.
"""

import random

def perturb_random(selected_columns, m, columns, num_remove=0, random_seed=None):
    """
    Perturb the solution by randomly removing N columns, then randomly adding columns until all rows are covered.

    Parameters:
    - selected_columns: list or set of currently selected column indices
    - m: number of rows in the instance
    - columns: list where columns[j] contains the rows covered by column j
    - num_remove: number of columns to remove before repair
    - random_seed: optional seed for reproducibility

    Returns:
    - tuple (feasible_selected, changed_indices) where:
      - feasible_selected: set of selected column indices after perturbation
      - changed_indices: set of columns removed or added during perturbation
    """
    if random_seed is not None:
        random.seed(random_seed)

    selected_set = set(selected_columns)
    selected_list = list(selected_set)
    if num_remove > len(selected_list):
        num_remove = len(selected_list)

    removed_indices = set(random.sample(selected_list, num_remove))
    selected_set -= removed_indices

    available_columns = set(range(len(columns))) - selected_set
    column_sets = [set(column) for column in columns]

    uncovered_rows = set(range(1, m + 1))
    for column_index in selected_set:
        uncovered_rows -= column_sets[column_index]

    added_indices = set()
    while uncovered_rows:
        candidate_columns = [
            column_index
            for column_index in available_columns
            if column_sets[column_index] & uncovered_rows
        ]

        if not candidate_columns:
            raise RuntimeError("No feasible completion found during perturbation.")

        chosen_column = random.choice(candidate_columns)
        selected_set.add(chosen_column)
        added_indices.add(chosen_column)
        available_columns.remove(chosen_column)
        uncovered_rows -= column_sets[chosen_column]

    changed_indices = removed_indices | added_indices
    return selected_set, changed_indices