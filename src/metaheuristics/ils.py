import random
import time
import math

from src.algorithms.pipelines import greedy_local_search
from src.heuristics.local_search_1opt import local_search_remove


def random_removal(selected_columns, num_remove):
    """
    Remove num_remove columns at random from the current solution.
    """
    if num_remove > len(selected_columns):
        num_remove = len(selected_columns)
    return set(random.sample(selected_columns, num_remove))


def greedy_from_partial(
    m,
    n,
    costs,
    columns,
    partial_selected,
    partial_objective_value,
    start_time=None,
    report=False,
    save_solution=None,
):
    """
    Perform greedy column selection starting from a partial solution.
    
    Continues greedily adding columns to cover uncovered rows,
    starting from the given partial solution.
    
    Parameters:
    - m: number of rows
    - n: number of columns
    - costs: list of costs for each column
    - columns: list where columns[j] contains rows covered by column j
    - partial_selected: set of column indices already selected
    - partial_objective_value: objective value of the partial selection
    
    Returns:
    - objective_value: total cost of the solution
    - selected_columns: list of selected column indices
    """
    # Ground set uncovered elements
    uncovered = set(range(1, m + 1))
    
    # Start with the partial solution
    selected_columns = list(partial_selected)
    objective_value = partial_objective_value
    
    # Convert once to sets (much faster)
    column_sets = [set(col) for col in columns]
    
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
    
    if start_time is None:
        start_time = time.time()

    if report:
        elapsed = time.time() - start_time
        print(f"Feasible solution of value {objective_value} [time {elapsed:.3f}]")
    if report and save_solution is not None:
        try:
            save_solution(objective_value, selected_columns, elapsed)
        except TypeError:
            save_solution(objective_value, selected_columns)

    return objective_value, selected_columns


def ils_hill_climbing(
    m,
    n,
    costs,
    columns,
    num_remove=2,
    random_seed=None,
    max_iter=100,
    start_time=None,
    report=True,
    save_solution=None,
):
    """
    Iterated Local Search (ILS) for the Set Covering Problem.

    Steps:
      1. Start with greedy + local search solution
      2. Perturb by removing N random columns
      3. Repair by greedily adding columns starting from remaining ones + local search
      4. Accept only if solution improves (hill climbing)
      5. Repeat for max_iter iterations
    
    Parameters:
    - m: number of rows
    - n: number of columns  
    - costs: list of costs for each column
    - columns: list where columns[j] contains rows covered by column j
    - num_remove: number of columns to remove during perturbation
    - random_seed: random seed for reproducibility
    - max_iter: maximum number of iterations
    
    Returns:
    - best_obj: objective value of best solution found
    - best_selected: list of selected column indices
    """
    
    if random_seed is not None:
        random.seed(random_seed)

    if start_time is None:
        start_time = time.time()

    # 1. Initialization: compute initial greedy + local search solution
    best_obj, best_selected = greedy_local_search(
        m,
        n,
        costs,
        columns,
        start_time=start_time,
        report=False,
    )

    if report:
        elapsed = time.time() - start_time
        print(f"Feasible solution of value {best_obj} [time {elapsed:.3f}]")
        if save_solution is not None:
            try:
                save_solution(best_obj, best_selected, elapsed)
            except TypeError:
                save_solution(best_obj, best_selected)

    for it in range(max_iter):
        # --- PERTURBATION: Remove N random columns ---
        removal_set = random_removal(best_selected, num_remove)
        remaining_selected = set(best_selected) - removal_set

        # --- REPAIR: Greedy construction starting from remaining columns ---
        removed_cost = sum(costs[j] for j in removal_set)
        remaining_objective = best_obj - removed_cost

        obj_repaired, selected_repaired = greedy_from_partial(
            m,
            n,
            costs,
            columns,
            remaining_selected,
            remaining_objective,
            start_time=start_time,
            report=False,
            save_solution=save_solution,
        )

        # --- LOCAL SEARCH: Improve the repaired solution ---
        obj_improved, selected_improved = local_search_remove(
            m,
            costs,
            columns,
            selected_repaired,
            start_time=start_time,
            report=False,
            save_solution=save_solution,
        )

        # --- ACCEPTANCE: Hill climbing criterion ---
        if obj_improved < best_obj:
            best_obj = obj_improved
            best_selected = selected_improved
            if report:
                elapsed = time.time() - start_time
                print(f"Feasible solution of value {best_obj} [time {elapsed:.3f}]")
                if save_solution is not None:
                    try:
                        save_solution(best_obj, best_selected, elapsed)
                    except TypeError:
                        save_solution(best_obj, best_selected)

    return best_obj, best_selected


def ils_sa(
    m,
    n,
    costs,
    columns,
    num_remove=2,
    random_seed=None,
    max_iter=1000,
    initial_temperature=100.0,
    cooling_rate=0.995,
    min_temperature=1e-3,
    start_time=None,
    report=True,
    save_solution=None,
):
    """
    Iterated Local Search with Simulated Annealing acceptance criterion.
    """

    if random_seed is not None:
        random.seed(random_seed)

    if start_time is None:
        start_time = time.time()

    # --- INITIAL SOLUTION ---
    best_obj, best_selected = greedy_local_search(
        m,
        n,
        costs,
        columns,
        start_time=start_time,
        report=False,
    )

    # Current solution 
    current_obj = best_obj
    current_selected = best_selected.copy()
    temperature = initial_temperature

    if report:
        elapsed = time.time() - start_time
        print(f"Feasible solution of value {best_obj} [time {elapsed:.3f}]")
        if save_solution is not None:
            try:
                save_solution(best_obj, best_selected, elapsed)
            except TypeError:
                save_solution(best_obj, best_selected)

    iteration = 0

    while (iteration < max_iter and temperature > min_temperature):

        # --- PERTURBATION: Remove N random columns ---
        removal_set = random_removal(current_selected,num_remove,)

        remaining_selected = set(current_selected) - removal_set

        # --- REPAIR: Greedy construction starting from remaining columns ---

        removed_cost = sum(costs[j] for j in removal_set)

        remaining_objective = current_obj - removed_cost 


        obj_repaired, selected_repaired = greedy_from_partial(
            m,
            n,
            costs,
            columns,
            remaining_selected,
            remaining_objective,
            start_time=start_time,
            report=False,
            save_solution=save_solution,
        )

        # --- LOCAL SEARCH: Improve the repaired solution ---

        obj_candidate, selected_candidate = local_search_remove(
            m,
            costs,
            columns,
            selected_repaired,
            start_time=start_time,
            report=False,
            save_solution=save_solution,
        )

        # --- ACCEPTANCE: Simulated Annealing criterion ---
        delta = obj_candidate - current_obj

        if delta < 0:
            accept = True

        else:

            probability = math.exp(-delta / temperature)
            accept = random.random() < probability

        
        # Move to new solution if accepted
        if accept:
            current_obj = obj_candidate
            current_selected = selected_candidate.copy()

        # Update best solution
        if current_obj < best_obj:

            best_obj = current_obj
            best_selected = current_selected.copy()

            if report:
                elapsed = time.time() - start_time

                print(f"Feasible solution of value {best_obj} [time {elapsed:.3f}]")

                if save_solution is not None:
                    try:
                        save_solution(
                            best_obj,
                            best_selected,
                            elapsed,
                        )
                    except TypeError:
                        save_solution(
                            best_obj,
                            best_selected,
                        )

        # Cooling procedure
        temperature *= cooling_rate

        iteration += 1

    return best_obj, best_selected