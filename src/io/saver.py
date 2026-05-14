from src.io.writer import write_solution_file, update_results_csv


def make_solution_saver(instance_path, instance_name, output_dir, csv_path):
    """
    Build a callback that saves every feasible solution to disk and updates
    the corresponding results CSV.
    """

    counter = {"count": 1}

    def saver(objective_value, selected_columns, elapsed=None):
        write_solution_file(
            instance_path,
            counter["count"],
            objective_value,
            selected_columns,
            output_dir=output_dir,
        )
        update_results_csv(
            csv_path,
            instance_name,
            objective_value,
            elapsed if elapsed is not None else 0.0,
        )
        counter["count"] += 1

    return saver