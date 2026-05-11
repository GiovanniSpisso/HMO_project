import csv
import os

def write_solution_file(instance_path, solution_id, objective_value, selected_columns, output_dir="solutions"):
    """
    Write a .sol file in a chosen directory.
    """
    os.makedirs(output_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(instance_path))[0]
    sol_name = f"{base}.{solution_id}.sol"

    full_path = os.path.join(output_dir, sol_name)

    with open(full_path, "w") as f:
        f.write(f"{objective_value}\n")
        f.write(" ".join(map(str, selected_columns)) + "\n")

    return full_path

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
