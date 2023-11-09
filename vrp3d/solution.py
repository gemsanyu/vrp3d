from copy import deepcopy
from typing import List, Tuple

from order.order import Order
from packing.packing import add_items_to_box
from vrp3d.vrp3d import VRP3D




"""
    tour_list: tour of each vehicle
    packing_position: each vehicle has orders, each order has items, 
        each item has packing position in the vehicle's box
    weight_cost_list: weight cost for each vehicle
    distance_cost_list: travelled distance cost for each vehicle
"""
class Solution:
    def __init__(self, prob:VRP3D) -> None:
        self.prob = deepcopy(prob)
        self.tour_list: List[List[int]] = [[] for _ in range(prob.num_vehicle)]
        # self.packing_order_list: List[List[int]]
        # self.packing_position: List[List[List[Tuple[int]]]]
        self.weight_cost_list: List[float] = [0]*prob.num_vehicle
        self.distance_cost_list: List[float] = [0]*prob.num_vehicle
        # self.is_feasible: bool

    def append_order(self, order_i:int, vec_i:int) -> Tuple[bool]:
        vec = self.prob.vehicle_list[vec_i]
        order = self.prob.order_list[order_i]
        is_packing_feasible = add_items_to_box(vec.box, order.packed_item_list)
        # print("Packing", is_packing_feasible)
        if not is_packing_feasible:
            return False
        dist_mat = self.prob.distance_matrix
        prev_node_idx = self.tour_list[-1]
        node_idx = order_i + 1
        velocity = self.prob.velocity
        dist_to_order = dist_mat[prev_node_idx, node_idx]
        duration_to_order = dist_to_order/velocity
        if len(vec.arrival_time_list)==0:
            prev_arrival_time = 0
        else:
            prev_arrival_time = vec.arrival_time_list[-1]
        arrival_time_to_order = prev_arrival_time + duration_to_order
        dist_to_depot = dist_mat[node_idx,0]
        duration_to_depot = dist_to_depot/velocity
        arrival_time_to_depot = arrival_time_to_order + duration_to_depot
        if arrival_time_to_depot > vec.max_duration:
            return False
        # okay now it's feasible, time to really append
        self.tour_list[vec_i] += [order_i]
        vec.arrival_time_list += [arrival_time_to_depot]
        return True

    # # a side note, this can be totally vectorized by numpy
    # # or parallelized with numba, still lazy
    # def compute_distance_cost(self):
    #     prob = self.prob
    #     dist_mat = prob.distance_matrix
    #     self.distance_cost_list = [0]*prob.num_vehicle
    #     for i, tour in enumerate(self.tour_list):
    #         len_tour = len(tour)
    #         if len_tour == 0:
    #             continue
    #         prev_node_idx = 0
    #         for j in range(len_tour):
    #             node_idx = tour[j] + 1
    #             self.distance_cost_list[i] += dist_mat[prev_node_idx,node_idx]
    #             prev_node_idx = node_idx
    #         self.distance_cost_list[i] += dist_mat[prev_node_idx,0]
    #         self.distance_cost_list[i] *= prob.vehicle_list[i].cost_per_km

    # def compute_weight_cost(self):
    #     prob = self.prob 
    #     self.weight_cost_list = [0]*prob.num_vehicle
    #     for i, tour in enumerate(self.tour_list):
    #         total_weight = sum([prob.order_list[node_idx].weight for node_idx in tour])
    #         self.weight_cost_list[i] = prob.vehicle_list[i].compute_weight_cost(total_weight)

    # def compute_cost(self):
    #     self.compute_distance_cost()
    #     self.compute_weight_cost()

    # def compute_vehicle_cost(self, )

    