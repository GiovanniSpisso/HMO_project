import time

from src.heuristics.local_search_1opt import build_coverage, remove_column


def local_search_2opt(
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

    improved = True
    current_cost = sum(costs[j] for j in selected_set)

    while improved:
        improved = False

        for j_remove in list(selected_set):
            remove_cost = costs[j_remove]

            uncovered_after_removal = set()
            for r in columns[j_remove]:
                if coverage[r] <= 1:
                    uncovered_after_removal.add(r)

            if not uncovered_after_removal:
                remove_column(j_remove, columns, coverage, selected_set)
                improved = True
                current_cost -= remove_cost

                if report:
                    elapsed = time.time() - start_time
                    print(f"Feasible solution of value {current_cost} [time {elapsed:.3f}]")
                    if save_solution is not None:
                        try:
                            save_solution(current_cost, sorted(selected_set), elapsed)
                        except TypeError:
                            save_solution(current_cost, sorted(selected_set))

                break

            best_replacement = None
            best_replacement_cost = remove_cost

            for j_add in range(len(columns)):
                if j_add in selected_set:
                    continue

                if uncovered_after_removal.issubset(columns[j_add]):
                    replacement_cost = costs[j_add]
                    if replacement_cost < best_replacement_cost:
                        best_replacement_cost = replacement_cost
                        best_replacement = j_add

            if best_replacement is not None:
                remove_column(j_remove, columns, coverage, selected_set)

                selected_set.add(best_replacement)
                for r in columns[best_replacement]:
                    coverage[r] += 1

                current_cost += best_replacement_cost - remove_cost
                improved = True

                if report:
                    elapsed = time.time() - start_time
                    print(f"Feasible solution of value {current_cost} [time {elapsed:.3f}]")
                    if save_solution is not None:
                        try:
                            save_solution(current_cost, sorted(selected_set), elapsed)
                        except TypeError:
                            save_solution(current_cost, sorted(selected_set))

                break

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