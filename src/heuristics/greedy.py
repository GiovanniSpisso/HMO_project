import time


def greedy(m, n, costs, columns, start_time=None, report=True, save_solution=None):

    if start_time is None:
        start_time = time.time()

    # Ground set uncovered elements
    uncovered = set(range(1, m + 1))

    # Used to store the chosen subset (i.e. columns)
    selected_columns = [] # Contains indices
    objective_value = 0

    # Convert once to sets (much faster)
    column_sets = [set(col) for col in columns]

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
            # backward compatibility: accept save_solution(obj, selected)
            save_solution(objective_value, selected_columns)

    return objective_value, selected_columns