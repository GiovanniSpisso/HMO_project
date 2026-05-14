"""
Hill Climbing acceptance criterion for ILS.

Accepts a solution only if it improves the current best.
"""


def accept_hill_climbing(candidate_obj, best_obj):
    """
    Hill Climbing acceptance criterion.
    
    Accepts the candidate solution only if it improves (is better than) the best solution.
    
    Parameters:
    - candidate_obj: objective value of the candidate solution
    - best_obj: objective value of the current best solution
    
    Returns:
    - True if candidate is accepted, False otherwise
    """
    return candidate_obj < best_obj
