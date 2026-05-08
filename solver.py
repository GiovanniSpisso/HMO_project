import csv
import os
import time


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


def write_solution_file(instance_path, solution_id, objective_value, selected_columns):
    """
    Write a .sol file with:
    - first line: objective value
    - second line: 0-based selected column indices
    """
    base = os.path.splitext(os.path.basename(instance_path))[0]
    sol_name = f"{base}.{solution_id}.sol"

    with open(sol_name, "w") as f:
        f.write(f"{objective_value}\n")
        f.write(" ".join(map(str, selected_columns)) + "\n")

    return sol_name


# Placeholder heuristic that just takes all columns (not a real solution)
def heuristic(m, n, costs, columns):
    """
    Temporary feasible solution.
    """
    selected_columns = list(range(n))  
    objective_value = sum(costs)
    return objective_value, selected_columns


def update_results_csv(csv_path, instance_name, bound, elapsed):
    rows = []
    found = False

    if os.path.exists(csv_path):
        with open(csv_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["instance"] == instance_name:
                    row["best_primal_bound"] = str(bound)
                    row["time_seconds"] = f"{elapsed:.3f}"
                    found = True
                rows.append(row)

    if not found:
        rows.append({
            "instance": instance_name,
            "best_primal_bound": str(bound),
            "time_seconds": f"{elapsed:.3f}",
        })

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["instance", "best_primal_bound", "time_seconds"])
        writer.writeheader()
        writer.writerows(rows)

        
def solve_instance(instance_path):
    """
    Main solver entry point.

    Must:
    - print feasible solution lines
    - save each incumbent to a .sol file
    """
    start = time.time()

    m, n, costs, columns = parse_instance(instance_path)
    instance_name = os.path.splitext(os.path.basename(instance_path))[0]

    best_objective = None
    best_columns = None
    solution_count = 1

    # Placeholder: no real heuristic yet, just a dummy solution that takes all columns
    obj, selected = heuristic(m, n, costs, columns)

    write_solution_file(instance_path, solution_count, obj, selected)

    elapsed = time.time() - start
    print(f"Feasible solution of value {obj} [time {elapsed:.3f}]")

    update_results_csv("results.csv", instance_name, obj, elapsed)