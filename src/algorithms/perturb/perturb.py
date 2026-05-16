"""
Perturbation function for ILS: removes N random columns
"""

import random


def perturb(selected_columns, num_remove, random_seed=None):
    """
    Perturb the solution by removing N random columns.

    Parameters:
    - selected_columns: list or set of currently selected column indices
    - num_remove: number of columns to remove
    - random_seed: optional seed for reproducibility

    Returns:
    - tuple (remaining_selected, removed_indices) where:
      - remaining_selected: set of columns still in the solution
      - removed_indices: set of removed column indices
    """
    if random_seed is not None:
        random.seed(random_seed)

    if num_remove > len(selected_columns):
        num_remove = len(selected_columns)

    removal_set = set(random.sample(list(selected_columns), num_remove))
    remaining_selected = set(selected_columns) - removal_set

    return remaining_selected, removal_set
