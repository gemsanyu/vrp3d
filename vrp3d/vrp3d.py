from typing import List, Tuple, Optional

import numpy as np
from sklearn.metrics.pairwise import haversine_distances

from vehicle.order import Order
from vehicle.vehicle import Vehicle

class VRP3D:
    def __init__(self,
                vehicle_list: List[Vehicle],
                order_list: List[Order],
                depot_coord: Tuple[float,float],
                distance_matrix: Optional[List[List[float]]] = None):
        self.vehicle_list = vehicle_list
        self.order_list = order_list
        self.coords = [depot_coord]
        self.coords += [order.coord for order in order_list]
        self.coords = np.asanyarray(self.coords, dtype=float)
        if distance_matrix is not None:
            self.distance_matrix = np.asanyarray(distance_matrix,dtype=float)
        else:
            self.distance_matrix = haversine_distances(self.coords).astype(float)
    
    # def compute_cost()