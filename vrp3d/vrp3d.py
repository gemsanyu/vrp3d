from typing import List, Tuple, Optional, Dict

import numpy as np
from sklearn.metrics.pairwise import haversine_distances

from item.item import Item
from order.order import Order
from vehicle.vehicle import Vehicle
from vrp3d.solution import Solution


class VRP3D:
    def __init__(self,
                vehicle_list: List[Vehicle],
                order_list: List[Order],
                depot_coord: Tuple[float,float],
                distance_matrix: Optional[List[List[float]]] = None,
                velocity:int=40):
        self.vehicle_list: List[Vehicle] = vehicle_list
        # we sort vehicle based on their worthiness.
        # no idea what it actually is, now its just 
        # average of cost per kg and cost per km
        self.vehicle_list = sorted(vehicle_list, key=lambda vhc: (vhc.cost_per_kg+vhc.cost_per_km)/2)

        self.order_list: List[Order] = order_list
        self.num_vehicle = len(vehicle_list)
        self.num_order = len(order_list)
        self.coords = [depot_coord]
        self.coords += [order.coord for order in order_list]
        self.coords = np.asanyarray(self.coords, dtype=float)
        if distance_matrix is not None:
            self.distance_matrix = np.asanyarray(distance_matrix,dtype=float)
        else:
            self.distance_matrix = haversine_distances(self.coords).astype(float) * 6371000/1000 #earth's radius in KM
        self.velocity = velocity
        self.driving_duration_matrix = self.distance_matrix/velocity
        self.item_dict: Dict[str, Item] = {}
        for order in order_list:
            for item in order.packed_item_list:
                self.item_dict[item.id] = item

    # """
    #     reset the objects to its initial state,
    #     or to the state of a solution
    # """
    # def reset(self, solution:Optional[Solution]=None):
    #     for i, vec in enumerate(self.vehicle_list):
    #         tour_list = solution.tour_list[i]
    #         packed_items = []
    #         self.vehicle_list[i].box.reset(

    #         )
    # def compute_cost(self, solution:Solution):
    #     if not solution.is_feasible:
    #         return 999999999
    #     weight_cost = sum([vec.weight_cost for vec in solution.vehicle_list])
    #     distance_cost = 