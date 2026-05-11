from src.heuristics.local_search import local_search_remove
from src.heuristics.greedy import greedy

def greedy_local_search(m, n, costs, columns):

    # initial solution
    obj, selected = greedy(m, n, costs, columns)

    # improve solution
    obj, selected = local_search_remove(
        m,
        costs,
        columns,
        selected
    )

    return obj, selected