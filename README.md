# HMO Project

This repository contains our solver for the **Heuristics for Mathematical Optimization** project on the Set Covering Problem.

## Repository structure

TO DO


### Linux
If needed, make the solver executable:

```bash
chmod +x sc_solver
```

###  Eleonora Notes:
From the tests we see that:
- Local Search (LS) of type 1-opt is too expensive in terms of running time, and rarely gives us significant improvements in the current considered solution. So we have decided to remove this kind of neighbourhood from the LS procedure.
- Since for high dimensional instances the Greedy (GR) algorithm is very expensive and slow, we have decide to consider only the Hill Climbing (HC) procedure in the Iterated Local Search (ILS) algorithm we have implement. So, we finally removed the last technique of Simulating Annealing (SA) in the ILS algorithm.
- We have created two tipe of possible perturbation:
    1. Random Perturbation (RP): we randomly remove some columns from the current solution, and then we randomly add new columns until feasibility of the solution is reached
    2. Greedy Perturbation (GP): we randomly remove some columns from the current solution, and then we repair the feasibility with the greedy strategy
- GP enforces the randomness of the algorithm, but it is too slow. So, in the end we have decided to keep GP mechanism.
- We select the number of colums to randomly remove in the GP strategy according to the size of the current instance. In particular, we did a tuning of the percentage of colums (as an hyperparameter) to been removed in the current solution. 