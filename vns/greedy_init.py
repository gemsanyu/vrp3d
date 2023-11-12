from copy import deepcopy
from typing import NamedTuple, List

from vrp3d.solution import Solution
from vrp3d.vrp3d import VRP3D


class InsertionAction(NamedTuple):
    order_i: int
    vec_i: int
    cost: float


"""
    very easy greedy heuristic
    from the first order (no particular ordering),
        append it to the vehicle that results in the
        cheapest additional cost
    we apply the trick in the paper.
        feasibility checking is the most expensive,
        then we just sort them first based on the cost of insertion (if feasible)
        and retrieve from the cheapest one, then check feasibility
        the first feasible (must also be cheapest) is chosen, then continue
        to the next order
"""
def greedy_initialization(problem: VRP3D) -> Solution:
    solution = Solution(problem)
    order_list = problem.order_list
    vehicle_list = problem.vehicle_list
    dist_mat = problem.distance_matrix
    for i, order in enumerate(order_list):
        node_idx = i+1
        action_list: List[InsertionAction] = []        
        for j in range(problem.num_vehicle):    
            add_dist_cost = 0
            if len(solution.tour_list[j])==0:
                prev_node_idx = 0
            else:
                prev_node_idx = solution.tour_list[j][-1] + 1
            add_dist = dist_mat[prev_node_idx, node_idx] + dist_mat[node_idx,0] - dist_mat[prev_node_idx,0]
            add_dist_cost = add_dist*vehicle_list[j].cost_per_km
            add_weight_cost = order.weight*vehicle_list[j].cost_per_kg
            add_cost = add_dist_cost + add_weight_cost
            action_list += [InsertionAction(i,j,add_cost)] 
        action_list = sorted(action_list, key=lambda action: action.cost)

        # check feasibility
        for action in action_list:
            new_sol = deepcopy(solution)
            is_insertion_feasible = new_sol.append_order(action.order_i, action.vec_i)
            # print(is_insertion_feasible)
            if is_insertion_feasible:
                solution = new_sol
                break
    return solution