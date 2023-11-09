from vns.greedy_init import greedy_initialization
from vrp3d.solution import Solution
# from vrp3d.utils import is_tour_feasible
from vrp3d.vrp3d import VRP3D

"""
    This algorithm is the method to generate initial solutions
    1. Start by greedily assigning orders to vehicles.
    2. Then try to combine each route with four options
        a. merge A + B
        b. merge A + reverse(B)
        c. merge reverse(A) + B
        d. merge reverse(A) + reverse(B)
    3. after two routes are merged, select the cheapest and
    feasible vehicle out of the two original vehicles.
    4. repeat this until no feasible merging is improving.
"""
def saving(problem: VRP3D) -> Solution:
    solution = greedy_initialization(problem)    