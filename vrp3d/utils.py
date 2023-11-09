from typing import List, Tuple

import numpy as np

from item.item import Item
from order.order import Order
from packing.packing import pack_items_to_boxes
from vehicle.vehicle import Vehicle

# check if a tour is feasible
# if the items can be packed inside the vehicle
# if the vehicle tour length not exceeding its max length
def is_tour_feasible(tour: List[int], vehicle:Vehicle, order_list: List[Order], dist_mat: np.ndarray):
    vehicle.box.reset()
    # set packing order for the orders in the tour
    item_list: List[Item] = []
    for i, node_idx in enumerate(tour):
        for j, item in enumerate(order_list[node_idx].packed_item_list):
            order_list[node_idx].packed_item_list[j].packing_order = i
        item_list += order_list[node_idx].packed_item_list
    used_box, unpacked_items = pack_items_to_boxes([vehicle.box], item_list, is_best_fit=False)
    if len(unpacked_items)>0:
        return False

    tour_length = 0
    for i, node_idx in enumerate(tour):
        
    