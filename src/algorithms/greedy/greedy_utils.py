"""
Utility functions for the greedy algorithm.
"""


def convert_to_sets(columns):
    """
    Convert columns list to sets for faster operations.
    
    Parameters:
    - columns: list where columns[j] contains rows covered by column j
    
    Returns:
    - list of sets where each set contains rows covered by that column
    """
    return [set(col) for col in columns]
