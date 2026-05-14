import time


def build_coverage(m, columns, selected_columns):
    """
    Build a coverage counter for each row of the ground set.
    """

    coverage = [0] * (m + 1)

    for j in selected_columns:
        for r in columns[j]:
            coverage[r] += 1

    return coverage


def can_remove_column(col_idx, columns, coverage):
    for r in columns[col_idx]:
        if coverage[r] <= 1:
            return False

    return True


def remove_column(col_idx, columns, coverage, selected_set):
    selected_set.remove(col_idx)

    for r in columns[col_idx]:
        coverage[r] -= 1


def local_search_remove(
    m,
    costs,
    columns,
    selected_columns,
    start_time=None,
    report=False,
    save_solution=None,
):
    if start_time is None:
        start_time = time.time()

    selected_set = set(selected_columns)
    coverage = build_coverage(m, columns, selected_set)
    current_cost = sum(costs[j] for j in selected_set)

    improved = True

    while improved:

        improved = False

        for j in list(selected_set):

            if can_remove_column(j, columns, coverage):

                remove_column(j, columns, coverage, selected_set)
                current_cost -= costs[j]

                improved = True

                if report:
                    elapsed = time.time() - start_time
                    print(f"Feasible solution of value {current_cost} [time {elapsed:.3f}]")
                    if save_solution is not None:
                        try:
                            save_solution(current_cost, sorted(selected_set), elapsed)
                        except TypeError:
                            save_solution(current_cost, sorted(selected_set))

    selected_columns = sorted(selected_set)
    elapsed = time.time() - start_time

    if report:
        print(f"Feasible solution of value {current_cost} [time {elapsed:.3f}]")
    if report and save_solution is not None:
        try:
            save_solution(current_cost, selected_columns, elapsed)
        except TypeError:
            save_solution(current_cost, selected_columns)

    return current_cost, selected_columns