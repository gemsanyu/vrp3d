from typing import List, Tuple, Optional

import numpy as np
from sklearn.metrics.pairwise import haversine_distances

from order.order import Order
from vehicle.vehicle import Vehicle


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


    # def compute_cost(self, solution:Solution):
    #     if not solution.is_feasible:
    #         return 999999999
    #     weight_cost = sum([vec.weight_cost for vec in solution.vehicle_list])
    #     distance_cost = 