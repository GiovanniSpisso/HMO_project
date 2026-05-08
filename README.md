# HMO Project

This repository contains our solver for the **Heuristics for Mathematical Optimization** project on the Set Covering Problem.

## Repository structure

- `sc_solver`  
  Main executable script. The evaluator runs this file directly.

- `solver.py`  
  Contains the main logic of the solver:
  - instance parsing
  - heuristic procedure
  - writing `.sol` files
  - updating `results.csv`

- `solution_checker.py`  
  Script used to verify whether a solution file is valid for a given instance.

- `results.csv`  
  CSV file containing, for each solved instance:
  - the best primal bound found
  - the time at which it was found


### Linux
If needed, make the solver executable:

```bash
chmod +x sc_solver