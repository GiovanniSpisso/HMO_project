"""
Simulated Annealing acceptance criterion for ILS.

Accepts a solution based on a probabilistic criterion that depends on temperature.
"""

import math
import random


def accept_simulated_annealing(candidate_obj, current_obj, temperature, min_temperature=1e-6):
    """
    Simulated Annealing acceptance criterion.
    
    Accepts the candidate solution with probability:
    - 1.0 if it improves the current solution (candidate_obj < current_obj)
    - exp(-delta / temperature) otherwise, where delta = candidate_obj - current_obj
    
    Parameters:
    - candidate_obj: objective value of the candidate solution
    - current_obj: objective value of the current solution
    - temperature: current temperature (decreases over time)
    - min_temperature: minimum temperature threshold (default: 1e-3)
    Returns:
    - True if candidate is accepted, False otherwise
    """
    delta = candidate_obj - current_obj
    
    if delta < 0:
        return True
    elif temperature <= min_temperature:
        return False
    else:
        probability = math.exp(-delta / temperature)
        return random.random() < probability
