def parse_instance(path):
    """
    Read an ORlib set covering instance.

    Expected format:
    - first line: m n
    - then n lines, one per column:
      cost, number_of_rows_covered, list_of_covered_rows (1-based)
    """
    with open(path, "r") as f:
        first = f.readline().split()
        m, n = map(int, first)

        costs = []
        columns = []
        for _ in range(n):
            data = list(map(int, f.readline().split()))
            cost = data[0]
            k = data[1]
            rows = data[2:2 + k]
            costs.append(cost)
            columns.append(rows)

    return m, n, costs, columns