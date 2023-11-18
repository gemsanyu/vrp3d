from typing import List

import numpy as np

from vrp3d.solution import Solution
from vrp3d.vrp3d import VRP3D
"""
    if we have fixed routes, 
    then we can do 1 last attempt
    to optimize the route
    if the route happens to have <=32 nodes to visit
"""
def backtrack(memo: np.ndarray, current_node_idx:int, binmask: int):
    pass

def dp(memo: np.ndarray, 
       is_visited: np.ndarray, 
       node_idx_list: np.ndarray,
       current_node_idx:int,
       bin_mask: int,
       distance_matrix: np.ndarray):
    if is_visited[current_node_idx,bin_mask]:
        return memo[current_node_idx,bin_mask]
    all_node_binmask = 2**(len(node_idx_list)+1)-1
    print(all_node_binmask)
    exit()

def get_improved_tour(tour:List[int], distance_matrix: np.ndarray, original_distance_cost: float, cost_per_km: float):
    tour = [node+1 for node in tour]
    tour = [0] + tour
    tour = np.asanyarray(tour, dtype=int)
    print(tour)
    all_node_binmask = 2**(len(tour)+1)-1
    print(all_node_binmask)
    exit()
    

def improve_tours_by_dp(solution: Solution, problem: VRP3D):
    problem.reset(solution)
    for i in range(solution.num_vehicle):
        if not solution.tour_list[i] or len(solution.tour_list[i])>31:
            continue
        original_distance_cost = problem.distance_cost_list[i]
        tour = get_improved_tour(solution.tour_list[i], 
                                 problem.distance_matrix, 
                                 original_distance_cost, 
                                 problem.vehicle_list[i].cost_per_km)
