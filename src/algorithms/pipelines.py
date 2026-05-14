import time

from src.heuristics.greedy import greedy
from src.heuristics.local_search_1opt import local_search_remove
from src.heuristics.local_search_2opt import local_search_2opt


def greedy_local_search(m, n, costs, columns, start_time=None, report=True, save_solution=None):

    if start_time is None:
        start_time = time.time()

    obj, selected = greedy(m, n, costs, columns, start_time=start_time, report=report)

    obj, selected = local_search_remove(
        m,
        costs,
        columns,
        selected,
        start_time=start_time,
        report=report,
        save_solution=save_solution,
    )

    if report:
        elapsed = time.time() - start_time
        print(f"Feasible solution of value {obj} [time {elapsed:.3f}]")
        if save_solution is not None:
            try:
                save_solution(obj, selected, elapsed)
            except TypeError:
                save_solution(obj, selected)

    return obj, selected


def greedy_local_search_2opt(m, n, costs, columns, start_time=None, report=True, save_solution=None):

    if start_time is None:
        start_time = time.time()

    obj, selected = greedy(m, n, costs, columns, start_time=start_time, report=report)

    obj, selected = local_search_2opt(
        m,
        costs,
        columns,
        selected,
        start_time=start_time,
        report=report,
        save_solution=save_solution,
    )

    if report:
        elapsed = time.time() - start_time
        print(f"Feasible solution of value {obj} [time {elapsed:.3f}]")
        if save_solution is not None:
            try:
                save_solution(obj, selected, elapsed)
            except TypeError:
                save_solution(obj, selected)

    return obj, selected